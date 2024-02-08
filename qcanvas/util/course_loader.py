import asyncio
import itertools
import logging
from asyncio import Task
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Sequence, Coroutine, Any

from bs4 import BeautifulSoup, Tag
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker
from sqlalchemy.orm import selectinload, selectin_polymorphic

import qcanvas.db as db
import qcanvas.queries as queries
from qcanvas.net.canvas import CanvasClient
from qcanvas.util.linkscanner.resource_scanner import ResourceScanner
from qcanvas.util.task_pool import TaskPool

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
    page: queries.Page | queries.File
    course_id: str
    module_id: str
    position: int


@dataclass
class TransientResourceToPageLink:
    page_id: str
    resource_id: str

    def __hash__(self):
        return hash(self.page_id) ^ hash(self.resource_id)


def _scan_page_for_links(page: db.PageLike) -> list[Tag]:
    """
    Extracts hyperlinks from a PageLike object
    """
    soup = BeautifulSoup(page.content, 'html.parser')
    return list(soup.find_all('a'))


def _remove_up_to_date_pages(g_courses: Sequence[queries.Course], pages: Sequence[db.ModuleItem]) -> list[TransientModulePage]:
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
    pages_id_mapped = dict((x.id, x) for x in pages)

    result: list[TransientModulePage] = []

    for g_course in g_courses:
        for g_module in g_course.modules_connection.nodes:
            for item_position, g_moduleitem in enumerate(g_module.module_items):
                content = g_moduleitem.content

                if isinstance(content, queries.Page) or isinstance(content, queries.File):
                    if (
                            content.m_id not in pages_id_mapped
                            or content.updated_at.replace(tzinfo=None) > pages_id_mapped[content.m_id].updated_at
                    ):
                        result.append(TransientModulePage(content, g_course.m_id, g_module.q_id, item_position))
                    else:
                        _logger.debug("Page %s is already up to date", content.m_id)

    return result


async def _extract_file_info(link: Tag, scanner: ResourceScanner, course_id: str) -> db.Resource | None:
    """
    Extracts file info from `link` using `scanner` and assigns the course_id to the resulting resource.

    Parameters
    ----------
    link
        The html element to scan
    scanner
        The scanner to process the link with
    course_id
        The id of the course the file belongs to
    Returns
    -------
    db.Resource
        The resource if the link was processed successfully.
    None
        If processing failed
    """
    try:
        _logger.debug(f"Fetching info for file %s with scanner %s", scanner.extract_id(link), scanner.name)

        result = await scanner.extract_resource(link)
        result.course_id = course_id
        return result
    except BaseException as e:
        _logger.error(f"Failed to retrieve info for link %s: %s", scanner.extract_id(link), e)
        return None


async def _fetch_module_file_page(file: queries.File, resource: db.Resource, course_id: str,
                                  module_id: str, position: int) -> db.ModuleFile:
    _logger.debug(f"Creating page for module file %s %s", file.m_id, file.display_name)

    page = db.convert_file_page(file)
    page.module_id = module_id
    page.course_id = course_id
    page.position = position
    page.resources.append(resource)

    return page


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

            # vvvvv mess

            pages_to_update = _remove_up_to_date_pages(g_courses, existing_pages)
            module_items = await self._load_page_content(pages_to_update)
            module_pages = [module_page for module_page in module_items if isinstance(module_page, db.ModulePage)]

            for relation in await self._map_links_in_pages(module_pages):
                existing_relation = await session.get(
                        db.ResourceToModuleItemAssociation,
                        (relation.page_id, relation.resource_id)
                )

                if existing_relation is None:
                    session.add(
                        db.ResourceToModuleItemAssociation(
                            module_item_id=relation.page_id,
                            resource_id=relation.resource_id
                        )
                    )

            session.add_all(module_items)

            # ^^^^^ mess

            assignments = []

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
                    elif g_assignment.updated_at.replace(tzinfo=None) <= assignment.updated_at:
                        continue

                    assignment.name = g_assignment.name.strip("\t  ")
                    assignment.description = g_assignment.description
                    assignment.created_at = g_assignment.created_at
                    assignment.updated_at = g_assignment.updated_at
                    assignment.due_at = g_assignment.due_at
                    assignment.position = g_assignment.position

                    assignments.append(assignment)

            for relation in await self._map_links_in_pages(assignments):
                if await session.get(db.ResourceToAssignmentAssociation, (relation.page_id, relation.resource_id)) is None:
                    session.add(
                        db.ResourceToAssignmentAssociation(
                            assignment_id=relation.page_id,
                            resource_id=relation.resource_id
                        )
                    )

            session.add_all(self._resource_pool.results())

            await session.flush()

    def _add_resources_and_pages_to_taskpool(
            self,
            existing_pages: Sequence[db.ModuleItem],
            existing_resources: Sequence[db.Resource]
    ):
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
        tasks: list[Task[db.ModuleItem]] = []

        for page in pages:
            content = page.page

            if isinstance(content, queries.File):
                tasks.append(asyncio.create_task(self._load_module_file(content, page.course_id, page.module_id, page.position)))
            elif isinstance(content, queries.Page):
                tasks.append(asyncio.create_task(self.load_module_page(content, page.course_id, page.module_id, page.position)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

            return [task.result() for task in tasks]
        else:
            return []

    async def _load_module_file(self, g_file: queries.File, course_id: str, module_id: str, position : int) -> db.ModuleFile:
        _logger.debug(f"Loading module file %s %s", g_file.m_id, g_file.display_name)

        resource = await self._resource_pool.submit(
            f"canvas_{g_file.m_id}",  # to match the format used by canvas link extractor
            lambda: self._fetch_module_file_resource(g_file, course_id)
        )

        return await self._moduleitem_pool.submit(
            g_file.m_id,
            lambda: _fetch_module_file_page(g_file, resource, course_id, module_id, position)
        )

    async def _fetch_module_file_resource(self, file: queries.File, course_id: str) -> db.Resource:
        _logger.debug(f"Fetching file (for module file) %s %s", file.m_id, file.display_name)
        result = await self._client.get_file(file.m_id, course_id)
        resource = db.convert_file(file, result.size)
        resource.course_id = course_id

        return resource

    async def load_module_page(self, g_page: queries.Page, course_id: str, module_id: str, position: int) -> db.ModulePage:
        return await self._moduleitem_pool.submit(
            g_page.m_id,
            lambda: self._fetch_module_item_page(g_page, course_id, module_id, position)
        )

    async def _fetch_module_item_page(self, page: queries.Page, course_id: str, module_id: str, position: int) -> db.ModulePage:
        _logger.debug(f"Fetching module page %s %s", page.m_id, page.title)

        result = await self._client.get_page(page.m_id, course_id)

        page = db.convert_page(page, result.body)
        page.module_id = module_id
        page.course_id = course_id
        page.position = position

        return page

    async def _map_links_in_pages(self, items: Sequence[db.PageLike]) -> Sequence[TransientResourceToPageLink]:
        tasks = []

        for item in items:
            # Assignment descriptions may be null. Avoid creating extra tasks by checking here
            if item.content is None:
                continue

            tasks.append(asyncio.create_task(self._extract_links_from_page(item)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

            result = []
            for task in tasks:
                result.extend(task.result())
            return result
        else:
            return []

    async def _extract_links_from_page(self, page: db.PageLike) -> set[TransientResourceToPageLink]:
        _logger.debug(f"Scanning %s %s for files", page.id, page.name)
        tasks = []

        for link in _scan_page_for_links(page):
            tasks.append(asyncio.create_task(self._process_link(link, page.course_id)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

            task_results = [task.result() for task in tasks]

            return set(
                [
                    TransientResourceToPageLink(page_id=page.id, resource_id=result.id)
                    for result in task_results if result is not None
                ]
            )
        else:
            return set()

    async def _process_link(self, link: Tag, course_id: str) -> db.Resource | None:
        for scanner in self._link_scanners:
            if scanner.accepts_link(link):
                id = scanner.extract_id(link)

                return await self._resource_pool.submit(
                    id,
                    lambda: _extract_file_info(link, scanner, course_id)
                )

        return None