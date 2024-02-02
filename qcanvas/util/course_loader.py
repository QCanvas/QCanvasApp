import asyncio
import logging
from typing import Sequence

from bs4 import BeautifulSoup, Tag
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker
from sqlalchemy.orm import selectinload

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


class CourseLoader:
    link_scanners: Sequence[LinkedResourceHandler]
    sessionmaker: AsyncSessionMaker
    _resource_fetch_taskpool: TaskPool[db.Resource] = TaskPool()
    _module_item_fetch_taskpool: TaskPool[db.ModuleItem] = TaskPool()

    def __init__(self,
                 client: CanvasClient,
                 sessionmaker: AsyncSessionMaker,
                 link_scanners: Sequence[LinkedResourceHandler]):

        self.client = client
        self.link_scanners = link_scanners
        self.sessionmaker = sessionmaker

    async def load_courses_data(self, g_courses: Sequence[queries.Course]):
        tasks = []

        for g_course in g_courses:
            tasks.append(asyncio.create_task(self._load_course_data(g_course)))

        await asyncio.wait(tasks)
        await self.update_db()

    async def _load_course_data(self, g_course: queries.Course):
        _logger.debug("Loading course %s", g_course.name)

        course = await self._add_basic_data_for_course(g_course)

        self._module_item_fetch_taskpool.add_values(dict((x.id, x) for x in course.module_items))
        self._resource_fetch_taskpool.add_values(dict((x.id, x) for x in course.resources))

        await self._load_pages_for_course(g_course)

        await self._scan_pages_for_file_links(course.module_items)
        await self._scan_pages_for_file_links(course.assignments)

        return course

    async def _add_basic_data_for_course(self, g_course: queries.Course):
        async with self.sessionmaker.begin() as session:

            if (await session.get(db.Term, g_course.term.q_id)) is None:
                # Add term for course
                await session.merge(db.convert_term(g_course.term))

            # Create the course and assign the term
            course = await session.merge(db.convert_course(g_course), options=course_creation_eager_load)
            course.term_id = g_course.term.q_id

            # Add modules for course
            for g_module in g_course.modules_connection.nodes:
                module = db.convert_module(g_module)
                module.course_id = course.id
                await session.merge(module)

            # Add assignments for course
            for g_assignment in g_course.assignments_connection.nodes:
                assignment = db.convert_assignment(g_assignment)
                assignment.course_id = g_course.m_id
                await session.merge(assignment)

            return course

    async def _load_pages_for_course(self, g_course: queries.Course):
        tasks = []

        for g_module in g_course.modules_connection.nodes:
            for g_module_item in g_module.module_items:
                content = g_module_item.content

                if isinstance(content, queries.File):
                    tasks.append(asyncio.create_task(self._load_module_file(content, g_course, g_module)))
                elif isinstance(content, queries.Page):
                    tasks.append(asyncio.create_task(self.load_module_page(content, g_course, g_module)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

    async def _load_module_file(self, g_file: queries.File, g_course: queries.Course, g_module: queries.Module):
        _logger.debug(f"Loading module file %s %s", g_file.m_id, g_file.display_name)

        resource = await self._resource_fetch_taskpool.submit(
            f"canvas_{g_file.m_id}", # to match the format used by canvas link extractor
            lambda: self._fetch_module_file_resource(g_file, g_course.m_id)
        )

        await self._module_item_fetch_taskpool.submit(
            g_file.m_id,
            lambda: self._fetch_module_file_page(g_file, resource, g_course, g_module)
        )

    async def _fetch_module_file_resource(self, file: queries.File, course_id: str) -> db.Resource:
        _logger.debug(f"Fetching file (for module file) %s %s", file.m_id, file.display_name)
        result = await self.client.get_file(file.m_id, course_id)
        resource = db.convert_file(file, result.size)
        resource.course_id = course_id

        return resource

    async def _fetch_module_file_page(self, file: queries.File, resource: db.Resource, course: queries.Course,
                                      module: queries.Module) -> db.ModuleFile:
        _logger.debug(f"Creating page for module file %s %s", file.m_id, file.display_name)

        page = db.convert_file_page(file)
        page.module_id = module.q_id
        page.course_id = course.m_id
        page.resources.append(resource)

        return page

    async def _fetch_module_item_page(self, page: queries.Page, course: queries.Course,
                                      module: queries.Module) -> db.ModulePage:
        _logger.debug(f"Fetching module page %s %s", page.m_id, page.title)

        result = await self.client.get_page(page.m_id, course.m_id)

        page = db.convert_page(page, result.body)
        page.module_id = module.q_id
        page.course_id = course.m_id

        return page

    async def load_module_page(self, g_page: queries.Page, g_course: queries.Course, g_module: queries.Module):
        await self._module_item_fetch_taskpool.submit(
            g_page.m_id,
            lambda: self._fetch_module_item_page(g_page, g_course, g_module)
        )

    async def _scan_pages_for_file_links(self, pages: Sequence[db.PageLike]):
        tasks = []

        for page in pages:
            if not isinstance(page, db.PageLike):
                continue

            tasks.append(asyncio.create_task(self._scan_page(page)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

    async def _scan_page(self, page: db.PageLike):
        _logger.debug(f"Scanning %s %s for files", page.id, page.name)
        tasks = []

        # Assignment descriptions may be null
        if page.content is None:
            return

        for link in _scan_page_for_links(page):
            tasks.append(asyncio.create_task(self._add_scanned_resource_to_page(page, link)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

    async def _add_scanned_resource_to_page(self, page: db.PageLike, link: Tag):
        resource = await self._process_link(link, page.course_id)

        if resource is None or resource in page.resources:
            return

        _logger.debug(f"Found {resource.id} {resource.file_name} on page {page.id} {page.name}")

        page.resources.append(resource)

    async def _extract_file_info(self, link: Tag, scanner: LinkedResourceHandler, course_id: str):
        try:
            _logger.debug(f"Fetching info for file {scanner.extract_id(link)} with scanner {scanner}")

            result = await scanner.extract_resource(link)
            result.course_id = course_id
            return result
        except BaseException as e:
            _logger.error(f"Failed to retrieve info for link {scanner.extract_id(link)}: {e}")
            return None

    async def _process_link(self, link: Tag, course_id: str) -> db.Resource | None:
        for scanner in self.link_scanners:
            if scanner.accepts_link(link):
                id = scanner.extract_id(link)

                return await self._resource_fetch_taskpool.submit(
                    id,
                    lambda: self._extract_file_info(link, scanner, course_id)
                )

        return None

    async def update_db(self):
        async with self.sessionmaker.begin() as session:
            session.add_all(self._module_item_fetch_taskpool.results())
            session.add_all(self._resource_fetch_taskpool.results())
