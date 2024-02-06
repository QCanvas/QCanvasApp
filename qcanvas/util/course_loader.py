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
from qcanvas.util.linkscanner.link_scanner import LinkedResourceHandler
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


class TransientPageType(Enum):
    ASSIGNMENT = 0
    MODULE_PAGE = 1

    @staticmethod
    def get_type_of_page(page: db.PageLike):
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


def _scan_page_for_links(page: db.PageLike) -> list[Tag]:
    soup = BeautifulSoup(page.content, 'html.parser')
    return list(soup.find_all('a'))

def _remove_up_to_date_pages(g_courses: Sequence[queries.Course], _pages: Sequence[db.ModuleItem]) -> list[
    TransientModulePage]:
    pages_id_mapped = dict((x.id, x) for x in _pages)

    result: list[TransientModulePage] = []

    for g_course in g_courses:
        for g_module in g_course.modules_connection.nodes:
            for g_moduleitem in g_module.module_items:
                content = g_moduleitem.content

                if isinstance(content, queries.Page) or isinstance(content, queries.File):
                    if content.m_id not in pages_id_mapped or content.updated_at.replace(tzinfo=None) > pages_id_mapped[
                        content.m_id].updated_at:
                        result.append(TransientModulePage(content, g_course.m_id, g_module.q_id))

    return result


async def _extract_file_info(link: Tag, scanner: LinkedResourceHandler, course_id: str):
    try:
        _logger.debug(f"Fetching info for file {scanner.extract_id(link)} with scanner {scanner}")

        result = await scanner.extract_resource(link)
        result.course_id = course_id
        return result
    except BaseException as e:
        _logger.error(f"Failed to retrieve info for link {scanner.extract_id(link)}: {e}")
        return None


async def _fetch_module_file_page(file: queries.File, resource: db.Resource, course_id: str,
                                  module_id: str) -> db.ModuleFile:
    _logger.debug(f"Creating page for module file %s %s", file.m_id, file.display_name)

    page = db.convert_file_page(file)
    page.module_id = module_id
    page.course_id = course_id
    page.resources.append(resource)

    return page


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
            module_items = await self._load_page_content(pages_to_update)

            mapped_links = await self._map_links_in_pages(
                [module_page for module_page in module_items if isinstance(module_page, db.ModulePage)])

            for relation in mapped_links:
                if await session.get(db.ResourceToModuleItemAssociation,
                                     (relation.page_id, relation.resource_id)) is None:
                    session.add(db.ResourceToModuleItemAssociation(relation.page_id, relation.resource_id))

            session.add_all(module_items)
            session.add_all(self._resource_pool.results())

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

    def _add_resources_and_pages_to_taskpool(self, existing_pages: Sequence[db.ModuleItem],
                                             existing_resoruces: Sequence[db.Resource]):
        self._moduleitem_pool.add_values(dict((page.id, page) for page in existing_pages))
        self._resource_pool.add_values(dict((resource.id, resource) for resource in existing_resoruces))

    async def _load_page_content(self, pages: Sequence[TransientModulePage]) -> list[db.ModuleItem]:
        tasks: list[Task[db.ModuleItem]] = []

        for page in pages:
            content = page.page

            if isinstance(content, queries.File):
                tasks.append(asyncio.create_task(self._load_module_file(content, page.course_id, page.module_id)))
            elif isinstance(content, queries.Page):
                tasks.append(asyncio.create_task(self.load_module_page(content, page.course_id, page.module_id)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

            return [task.result() for task in tasks]
        else:
            return []

    async def _load_module_file(self, g_file: queries.File, course_id: str, module_id: str) -> db.ModuleFile:
        _logger.debug(f"Loading module file %s %s", g_file.m_id, g_file.display_name)

        resource = await self._resource_pool.submit(
            f"canvas_{g_file.m_id}",  # to match the format used by canvas link extractor
            lambda: self._fetch_module_file_resource(g_file, course_id)
        )

        return await self._moduleitem_pool.submit(
            g_file.m_id,
            lambda: _fetch_module_file_page(g_file, resource, course_id, module_id)
        )

    async def _fetch_module_file_resource(self, file: queries.File, course_id: str) -> db.Resource:
        _logger.debug(f"Fetching file (for module file) %s %s", file.m_id, file.display_name)
        result = await self._client.get_file(file.m_id, course_id)
        resource = db.convert_file(file, result.size)
        resource.course_id = course_id

        return resource

    async def load_module_page(self, g_page: queries.Page, course_id: str, module_id: str) -> db.ModulePage:
        return await self._moduleitem_pool.submit(
            g_page.m_id,
            lambda: self._fetch_module_item_page(g_page, course_id, module_id)
        )

    async def _fetch_module_item_page(self, page: queries.Page, course_id: str, module_id: str) -> db.ModulePage:
        _logger.debug(f"Fetching module page %s %s", page.m_id, page.title)

        result = await self._client.get_page(page.m_id, course_id)

        page = db.convert_page(page, result.body)
        page.module_id = module_id
        page.course_id = course_id

        return page

    async def _map_links_in_pages(self, items: Sequence[db.PageLike]) -> Sequence[TransientResourceToPageLink]:
        tasks = []

        for item in items:
            tasks.append(asyncio.create_task(self._extract_links_from_page(item)))

        if len(tasks) == 0:
            return []

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

            return set(
                [TransientResourceToPageLink(page_id=page.id, resource_id=result.id, page_type=page_type) for result in
                 task_results if result is not None])
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
