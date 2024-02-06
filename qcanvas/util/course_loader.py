import asyncio
import itertools
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Sequence

from bs4 import BeautifulSoup, Tag
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker
from sqlalchemy.orm import selectinload, selectin_polymorphic

import qcanvas.db as db
import qcanvas.queries as queries
from qcanvas.net.canvas import CanvasClient
from qcanvas.util.linkscanner.link_scanner import LinkedResourceHandler
from qcanvas.util.task_pool import TaskPool


def _scan_page_for_links(page: db.PageLike) -> list[Tag]:
    soup = BeautifulSoup(page.content, 'html.parser')
    return list(soup.find_all('a'))


_logger = logging.getLogger("course_loader")

course_creation_eager_load = [
    selectinload(db.Course.module_items)
    .selectin_polymorphic([db.ModulePage, db.ModulePage])
    .joinedload(db.ModuleItem.resources),
    selectinload(db.Course.modules),
    selectinload(db.Course.assignments)
    .joinedload(db.Assignment.resources),
    selectinload(db.Course.resources)
]


@dataclass
class TransientModulePage:
    page: queries.Page
    course_id: str
    module_id: str


class TransientPageType(Enum):
    ASSIGNMENT = 0
    MODULE_PAGE = 1

    @staticmethod
    def get_type_of_page(page : db.PageLike):
        if isinstance(page, db.ModulePage):
            return TransientPageType.MODULE_PAGE
        elif isinstance(page, db.Assignment):
            return TransientPageType.ASSIGNMENT
        else:
            raise TypeError("Expected page to be a module page or an assignment")


@dataclass
class TransientResourceToPageLink:
    page_id: str
    resource_id: str
    page_type: TransientPageType

    def __hash__(self):
        return hash(self.page_id) ^ hash(self.resource_id) ^ hash(self.page_type.value)


def _remove_up_to_date_pages(g_courses: Sequence[queries.Course], _pages: Sequence[db.ModuleItem]) -> list[
    TransientModulePage]:
    pages_id_mapped = dict((x.id, x) for x in _pages)

    result: list[TransientModulePage] = []

    for g_course in g_courses:
        for g_module in g_course.modules_connection.nodes:
            for g_moduleitem in g_module.module_items:
                content = g_moduleitem.content

                if isinstance(content, queries.Page):
                    if content.m_id not in pages_id_mapped or content.updated_at > pages_id_mapped[
                        content.m_id].updated_at:
                        result.append(TransientModulePage(content, g_course.m_id, g_module.q_id))

    return result


class CourseLoader:
    _link_scanners: Sequence[LinkedResourceHandler]
    _session_maker: AsyncSessionMaker

    _resource_pool: TaskPool[db.Resource]
    _moduleitem_pool: TaskPool[db.ModuleItem]

    def __init__(self,
                 client: CanvasClient,
                 sessionmaker: AsyncSessionMaker,
                 link_scanners: Sequence[LinkedResourceHandler],
                 last_update: datetime):

        self._client = client
        self._link_scanners = link_scanners
        self._session_maker = sessionmaker
        self._last_update = last_update

        self._resource_pool = TaskPool()
        self._moduleitem_pool = TaskPool()

    def _refresh_page_if_outdated(self, page: db.PageLike):
        return page.updated_at > self._last_update

    async def load_courses_data(self, g_courses: Sequence[queries.Course]):
        #################################
        # DO NOT SPLIT THIS FUNCTION UP # (or i will kill you :))) )
        #################################

        async with self._session_maker.begin() as session:
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

            pages_to_update = _remove_up_to_date_pages(g_courses, existing_pages)

            await self._load_page_content(pages_to_update)

            mapped_links = await self._map_links_in_pages(pages_to_update)

            for relation in mapped_links:
                if await session.get(db.ResourceToModuleItemAssociation, (relation.page_id, relation.resource_id)) is None:
                    session.add(db.ResourceToModuleItemAssociation(relation.page_id, relation.resource_id))


            for g_course in g_courses:
                term = await session.get(db.Term, g_course.term.q_id)

                if term is None:
                    term = db.convert_term(g_course.term)
                    session.add(term)

                course = await session.get(db.Course, g_course.m_id)

                if course is None:
                    course = db.Course()
                    course.id = g_course.m_id
                    session.add(course)

                course.name = g_course.name
                course.term = term

                for g_module in g_course.modules_connection.nodes:
                    module = await session.get(db.Module, g_module.q_id)

                    if module is None:
                        module = db.Module()
                        module.id = g_module.q_id
                        module.course_id = g_course.m_id
                        session.add(module)

                    module.name = g_module.name

                for g_assignment in g_course.assignments_connection.nodes:
                    assignment = await session.get(db.Assignment, g_assignment.q_id)

                    if assignment is None:
                        assignment = db.Assignment()
                        assignment.id = g_assignment.q_id
                        assignment.course_id = g_course.m_id
                        session.add(assignment)

                    assignment.name = g_assignment.name
                    assignment.description = g_assignment.description
                    assignment.created_at = g_assignment.created_at
                    assignment.updated_at = g_assignment.updated_at
                    assignment.due_at = g_assignment.due_at
                    assignment.position = g_assignment.position

            await session.flush()

            # await self._load_all_pages(g_courses)

    def _add_resources_and_pages_to_taskpool(self, existing_pages: Sequence[db.ModuleItem],
                                             existing_resoruces: Sequence[db.Resource]):
        self._moduleitem_pool.add_values(dict((page.id, page) for page in existing_pages))
        self._resource_pool.add_values(dict((resource.id, resource) for resource in existing_resoruces))

    async def _load_page_content(self, pages: Sequence[TransientModulePage]):
        tasks = []

        for page in pages:
            content = page.page

            if isinstance(content, queries.File):
                tasks.append(asyncio.create_task(self._load_module_file(content, page.course_id, page.module_id)))
            elif isinstance(content, queries.Page):
                tasks.append(asyncio.create_task(self.load_module_page(content, page.course_id, page.module_id)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

    async def _load_module_file(self, g_file: queries.File, course_id: str, module_id: str):
        _logger.debug(f"Loading module file %s %s", g_file.m_id, g_file.display_name)

        resource = await self._resource_pool.submit(
            f"canvas_{g_file.m_id}",  # to match the format used by canvas link extractor
            lambda: self._fetch_module_file_resource(g_file, course_id)
        )

        await self._moduleitem_pool.submit(
            g_file.m_id,
            lambda: self._fetch_module_file_page(g_file, resource, course_id, module_id)
        )

    # async def _load_all_pages(self, courses: Sequence[queries.Course]):
    #     tasks = []
    #
    #     for g_course in courses:
    #         for g_module in g_course.modules_connection.nodes:
    #             for g_module_item in g_module.module_items:
    #                 content = g_module_item.content
    #
    #                 if isinstance(content, queries.File):
    #                     tasks.append(asyncio.create_task(self._load_module_file(content, g_course, g_module)))
    #                 elif isinstance(content, queries.Page):
    #                     tasks.append(asyncio.create_task(self.load_module_page(content, g_course, g_module)))
    #
    #     if len(tasks) > 0:
    #         await asyncio.wait(tasks)

    #########################################################################################################################
    # async def _load_module_file(self, g_file: queries.File, g_course: queries.Course, g_module: queries.Module):
    #     _logger.debug(f"Loading module file %s %s", g_file.m_id, g_file.display_name)
    #
    #     resource = await self._resource_pool.submit(
    #         f"canvas_{g_file.m_id}",  # to match the format used by canvas link extractor
    #         lambda: self._fetch_module_file_resource(g_file, g_course.m_id)
    #     )
    #
    #     await self._moduleitem_pool.submit(
    #         g_file.m_id,
    #         lambda: self._fetch_module_file_page(g_file, resource, g_course, g_module)
    #     )

    async def _fetch_module_file_resource(self, file: queries.File, course_id: str) -> db.Resource:
        _logger.debug(f"Fetching file (for module file) %s %s", file.m_id, file.display_name)
        result = await self._client.get_file(file.m_id, course_id)
        resource = db.convert_file(file, result.size)
        resource.course_id = course_id

        return resource

    async def _fetch_module_file_page(self, file: queries.File, resource: db.Resource, course_id: str,
                                      module_id: str) -> db.ModuleFile:
        _logger.debug(f"Creating page for module file %s %s", file.m_id, file.display_name)

        page = db.convert_file_page(file)
        page.module_id = module_id
        page.course_id = course_id
        page.resources.append(resource)

        return page

    async def _fetch_module_item_page(self, page: queries.Page, course_id: str, module_id: str) -> db.ModulePage:
        _logger.debug(f"Fetching module page %s %s", page.m_id, page.title)

        result = await self._client.get_page(page.m_id, course_id)

        page = db.convert_page(page, result.body)
        page.module_id = module_id
        page.course_id = course_id

        return page

    async def load_module_page(self, g_page: queries.Page, course_id: str, module_id : str):
        await self._moduleitem_pool.submit(
            g_page.m_id,
            lambda: self._fetch_module_item_page(g_page, course_id, module_id)
        )

    # async def _scan_pages_for_file_links(self, pages: Sequence[db.PageLike]):
    #     tasks = []
    #
    #     for page in pages:
    #         if not isinstance(page, db.PageLike):
    #             continue
    #
    #         tasks.append(asyncio.create_task(self._scan_page(page)))
    #
    #     if len(tasks) > 0:
    #         await asyncio.wait(tasks)

    async def _map_links_in_pages(self, items : Sequence[TransientModulePage]) -> Sequence[TransientResourceToPageLink]:
        tasks = []

        for item in items:

            if isinstance(item, TransientModulePage):
                page_content = self._moduleitem_pool.get_completed_result(item.page.m_id)

                assert isinstance(page_content, db.PageLike)

                tasks.append(asyncio.create_task(self._extract_links_from_page(page_content)))
            # elif isinstance(item, queries.Assignment):
            #     tasks.append(asyncio.create_task(self._extract_links_from_page(item)))


        await asyncio.wait(tasks)

        result = []

        for task in tasks:
            result.extend(task.result())

        return result


    async def _extract_links_from_page(self, page: db.PageLike) -> set[TransientResourceToPageLink]:
        _logger.debug(f"Scanning %s %s for files", page.id, page.name)
        tasks = []

        # Assignment descriptions may be null
        if page.content is None:
            return set()

        for link in _scan_page_for_links(page):
            tasks.append(asyncio.create_task(self._process_link(link, page.course_id)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

            page_type = TransientPageType.get_type_of_page(page)
            task_results = [task.result() for task in tasks if task is not None]

            return set([TransientResourceToPageLink(page_id=page.id, resource_id=result.id, page_type=page_type) for result in task_results if result is not None])
        else:
            return set()

    # async def _scan_page(self, page: db.PageLike):
    #     _logger.debug(f"Scanning %s %s for files", page.id, page.name)
    #     tasks = []
    #
    #     # Assignment descriptions may be null
    #     if page.content is None:
    #         return
    #
    #     for link in _scan_page_for_links(page):
    #         tasks.append(asyncio.create_task(self._add_scanned_resource_to_page(page, link)))
    #
    #     if len(tasks) > 0:
    #         await asyncio.wait(tasks)

    # async def _add_scanned_resource_to_page(self, page: db.PageLike, link: Tag):
    #     resource = await self._process_link(link, page.course_id)
    #
    #     if resource is None or resource in page.resources:
    #         return
    #
    #     _logger.debug(f"Found {resource.id} {resource.file_name} on page {page.id} {page.name}")
    #
    #     page.resources.append(resource)

    async def _process_link(self, link: Tag, course_id: str) -> db.Resource | None:
        for scanner in self._link_scanners:
            if scanner.accepts_link(link):
                id = scanner.extract_id(link)

                return await self._resource_pool.submit(
                    id,
                    lambda: self._extract_file_info(link, scanner, course_id)
                )

        return None

    async def _extract_file_info(self, link: Tag, scanner: LinkedResourceHandler, course_id: str):
        try:
            _logger.debug(f"Fetching info for file {scanner.extract_id(link)} with scanner {scanner}")

            result = await scanner.extract_resource(link)
            result.course_id = course_id
            return result
        except BaseException as e:
            _logger.error(f"Failed to retrieve info for link {scanner.extract_id(link)}: {e}")
            return None

    # async def update_db(self):
    #     async with self._session_maker.begin() as session:
    #         session.add_all(self._module_item_fetch_taskpool.results())
    #         session.add_all(self._resource_fetch_taskpool.results())
