import asyncio
import logging
from asyncio import Task
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker, AsyncSession
from sqlalchemy.orm import selectin_polymorphic

import qcanvas.db as db
import qcanvas.queries as queries
from qcanvas.net.canvas import CanvasClient
from qcanvas.util.linkscanner.resource_scanner import ResourceScanner
from qcanvas.util.task_pool import TaskPool

import qcanvas.util.course_indexer.conversion_helpers as conv_helper
import qcanvas.util.course_indexer.resource_helpers as resource_helper

_logger = logging.getLogger("course_loader")


@dataclass
class TransientModulePage:
    page: queries.Page | queries.File
    course_id: str
    module_id: str
    position: int


def _prepare_out_of_date_pages_for_loading(g_courses: Sequence[queries.Course], pages: Sequence[db.ModuleItem]) -> list[TransientModulePage]:
    """
    Removes pages that are up-to-date from the pages list by comparing the last update time of the pages from the query
    to the last update time of the pages in the database.

    Parameters
    ----------
    g_courses
        The list of courses (with module items) to check for an update.
    pages
        The list of pages already existing in the database.
    Returns
    -------
    list[TransientModulePage]
        A list of pages that have had an update to them.
    """
    pages_id_mapped = {x.id: x for x in pages}

    result: list[TransientModulePage] = []

    for g_course in g_courses:
        for g_module in g_course.modules_connection.nodes:
            for item_position, g_moduleitem in enumerate(g_module.module_items):
                content = g_moduleitem.content

                if isinstance(content, queries.Page) or isinstance(content, queries.File):
                    # if (
                    #         content.m_id not in pages_id_mapped
                    #         or content.updated_at.replace(tzinfo=None) > pages_id_mapped[content.m_id].updated_at
                    # ):
                    result.append(TransientModulePage(content, g_course.m_id, g_module.q_id, item_position))
                    # else:
                    #     _logger.debug("Page %s is already up to date", content.m_id)

    return result


class CourseLoader:
    _link_scanners: Sequence[ResourceScanner]
    _session_maker: AsyncSessionMaker

    _resource_pool: TaskPool[db.Resource]
    _moduleitem_pool: TaskPool[db.ModuleItem]

    def __init__(self,
                 client: CanvasClient,
                 sessionmaker: AsyncSessionMaker,
                 link_scanners: Sequence[ResourceScanner],
                 last_update: datetime):

        self._client = client
        self._link_scanners = link_scanners
        self._session_maker = sessionmaker
        self._last_update = last_update

        self._resource_pool = TaskPool()
        self._moduleitem_pool = TaskPool()

    async def load_courses_data(self, g_courses: Sequence[queries.Course]):
        async with self._session_maker.begin() as session:
            await self._load_module_items(g_courses, session)

            assignments = []

            for g_course in g_courses:
                term = await conv_helper.create_term(g_course, session)
                await conv_helper.create_course(g_course, session, term)
                await conv_helper.create_modules(g_course, session)
                assignments.extend(await conv_helper.create_assignments(g_course, session))

            await resource_helper.create_assignment_resource_relations(
                await resource_helper.map_links_in_pages(
                    self._link_scanners,
                    self._resource_pool,
                    assignments
                ),
                session
            )

            session.add_all(self._resource_pool.results())

    async def _load_module_items(self, g_courses: Sequence[queries.Course], session: AsyncSession):
        # Get the ids of all the courses we are going to index/load
        course_ids = [g_course.m_id for g_course in g_courses]

        existing_pages = (await session.execute(
            select(db.ModuleItem)
            .where(db.ModuleItem.course_id.in_(course_ids))
            .options(selectin_polymorphic(db.ModuleItem, [db.ModulePage]))
        )).scalars().all()

        existing_resources = (await session.execute(
            select(db.Resource)
            .where(db.Resource.course_id.in_(course_ids))
        )).scalars().all()

        self._add_resources_and_pages_to_taskpool(existing_pages, existing_resources)

        pages_to_update = _prepare_out_of_date_pages_for_loading(g_courses, existing_pages)
        module_items = await self._load_page_content(pages_to_update)

        await resource_helper.create_module_item_resource_relations(
            await resource_helper.map_links_in_pages(
                self._link_scanners,
                self._resource_pool,
                list(filter(lambda x: isinstance(x, db.PageLike), module_items))
            ),
            session
        )

        session.add_all(module_items)

    def _add_resources_and_pages_to_taskpool(self, existing_pages: Sequence[db.ModuleItem],
                                             existing_resources: Sequence[db.Resource]):
        self._moduleitem_pool.add_values(dict((page.id, page) for page in existing_pages))
        self._resource_pool.add_values(dict((resource.id, resource) for resource in existing_resources))

    async def _load_page_content(self, pages: Sequence[TransientModulePage]) -> list[db.ModuleItem]:
        """
        Loads the page content for the specified pages
        Parameters
        ----------
        pages
            The pages to load
        Returns
        -------
            The list of complete pages with page content loaded.
        """
        tasks: list[Task[db.ModuleItem | None]] = []

        for page in pages:
            content = page.page

            if isinstance(content, queries.File):
                tasks.append(
                    asyncio.create_task(self._load_module_file(content, page.course_id, page.module_id, page.position)))
            elif isinstance(content, queries.Page):
                tasks.append(
                    asyncio.create_task(self.load_module_page(content, page.course_id, page.module_id, page.position)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

            return [task.result() for task in tasks if task.result() is not None]
        else:
            return []

    async def _load_module_file(self, g_file: queries.File, course_id: str, module_id: str,
                                position: int) -> db.ModuleFile:
        _logger.debug(f"Loading module file %s %s", g_file.m_id, g_file.display_name)

        resource = await self._resource_pool.submit(
            f"canvas_{g_file.m_id}",  # to match the format used by canvas link extractor
            lambda: self._fetch_module_file_resource(g_file, course_id)
        )

        return await self._moduleitem_pool.submit(
            g_file.m_id,
            lambda: self._fetch_module_file_page(g_file, resource, course_id, module_id, position)
        )

    async def _fetch_module_file_resource(self, file: queries.File, course_id: str) -> db.Resource:
        _logger.debug(f"Fetching file (for module file) %s %s", file.m_id, file.display_name)
        result = await self._client.get_file(file.m_id, course_id)
        resource = db.convert_file(file, result.size)
        resource.course_id = course_id

        return resource

    async def load_module_page(self, g_page: queries.Page, course_id: str, module_id: str,
                               position: int) -> db.ModulePage | None:
        return await self._moduleitem_pool.submit(
            g_page.m_id,
            lambda: self._fetch_module_item_page(g_page, course_id, module_id, position)
        )

    async def _fetch_module_item_page(self, page: queries.Page, course_id: str, module_id: str,
                                      position: int) -> db.ModulePage | None:
        _logger.debug("Fetching module page %s %s", page.m_id, page.title)

        try:
            result = await self._client.get_page(page.m_id, course_id)
        except httpx.HTTPStatusError as e:
            _logger.warning(e)
            return None

        if result.locked_for_user:
            _logger.warning("Page %s %s is locked", page.m_id, page.title)
            return None

        page = db.convert_page(page, result.body)
        page.module_id = module_id
        page.course_id = course_id
        page.position = position

        return page

    @staticmethod
    async def _fetch_module_file_page(file: queries.File, resource: db.Resource, course_id: str,
                                      module_id: str, position: int) -> db.ModuleFile:
        _logger.debug(f"Creating page for module file %s %s", file.m_id, file.display_name)

        page = db.convert_file_page(file)
        page.module_id = module_id
        page.course_id = course_id
        page.position = position
        page.resources.append(resource)

        return page
