import asyncio
from typing import Sequence

from bs4 import BeautifulSoup, Tag
from httpx import HTTPStatusError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

import qcanvas.db as db
import qcanvas.queries as queries
from qcanvas.net.canvas import CanvasClient
from qcanvas.util.link_scanner import LinkedResourceHandler
from qcanvas.util.task_pool import TaskPool


def scan_page_for_links(page: db.ModulePage) -> set[Tag]:
    soup = BeautifulSoup(page.content, 'html.parser')
    result: set[Tag] = set()

    for link in soup.find_all('a'):
        result.add(link)

    return result


class ModuleItemLoader:
    link_scanners: Sequence[LinkedResourceHandler]

    resource_fetch_taskpool: TaskPool[db.Resource] = TaskPool()
    module_item_fetch_taskpool: TaskPool[db.ModuleItem] = TaskPool()

    def __init__(self, existing_module_items: Sequence[db.ModuleItem], existing_resources: Sequence[db.Resource],
                 client: CanvasClient,
                 link_scanners: Sequence[LinkedResourceHandler]):
        self.module_item_fetch_taskpool.add_completed_values(
            dict((module_item.id, module_item) for module_item in existing_module_items))
        self.resource_fetch_taskpool.add_completed_values(
            dict((resource.id, resource) for resource in existing_resources))

        self.client = client
        self.link_scanners = link_scanners

    async def _fetch_module_file_resource(self, file: queries.File, course_id: str) -> db.Resource:
        result = await self.client.get_file(file.m_id, course_id)
        resource = db.convert_file(file, result.size)
        resource.course_id = course_id

        return resource

    async def _fetch_module_file_page(self, file: queries.File, resource: db.Resource, course: queries.Course,
                                      module: queries.Module) -> db.ModuleFile:
        page = db.convert_file_page(file)
        page.module_id = module.q_id
        page.course_id = course.m_id
        page.resources.append(resource)

        return page

    async def load_module_file(self, g_file: queries.File, g_course: queries.Course, g_module: queries.Module):
        file_id = f"canvas_{g_file.m_id}"

        resource = await self.resource_fetch_taskpool.submit(
            file_id,
            lambda: self._fetch_module_file_resource(g_file, g_course.m_id)
        )

        await self.module_item_fetch_taskpool.submit(
            g_file.m_id, # don't use file_id
            lambda: self._fetch_module_file_page(g_file, resource, g_course, g_module)
        )

    async def _fetch_module_item_page(self, page: queries.Page, course: queries.Course,
                                      module: queries.Module) -> db.ModulePage:
        result = await self.client.get_page(page.m_id, course.m_id)

        page = db.convert_page(page, result.body)
        page.module_id = module.q_id
        page.course_id = course.m_id

        return page

    async def load_module_page(self, g_page: queries.Page, g_course: queries.Course, g_module: queries.Module):
        await self.module_item_fetch_taskpool.submit(
            g_page.m_id,
            lambda: self._fetch_module_item_page(g_page, g_course, g_module)
        )

    # fixme this is kinda shitty
    async def scan_pages_for_file_links(self):
        tasks = []
        # store it here so it doesn't change
        pages = self.module_item_fetch_taskpool.results()

        for page in pages:
            if not isinstance(page, db.ModulePage):
                continue

            # print(f"Now scanning page {page.name}")

            tasks.append(asyncio.create_task(self.do_thing(page)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

    async def do_thing(self, page: db.ModulePage):
        async def task(link, obj):
            await obj.add_scanned_resource_to_page(page, await obj.process_link(link, page.course_id))

        tasks = []

        for link in scan_page_for_links(page):
            tasks.append(asyncio.create_task(task(link, self)))

        if len(tasks) > 0:
            await asyncio.wait(tasks)

    async def add_scanned_resource_to_page(self, page: db.ModulePage, resource: db.Resource | None):
        if resource is None or resource in page.resources:
            return

        page.resources.append(resource)

        # print(f"{resource.id} -> {page.id}")
        # print(f"Found {resource.friendly_name} for {page.name} ({resource.course_id})")

    async def _extract_file_info(self, link: Tag, scanner: LinkedResourceHandler, course_id: str):
        try:
            result = await scanner.extract_resource(link)
            result.course_id = course_id
            # print(f"Found {result.friendly_name}")
            return result
        except HTTPStatusError:
            return None

    async def process_link(self, link: Tag, course_id: str) -> db.Resource | None:
        for scanner in self.link_scanners:
            if scanner.accepts_link(link):
                id = scanner.extract_id(link)

                return await self.resource_fetch_taskpool.submit(
                    id,
                    lambda: self._extract_file_info(link, scanner, course_id)
                )

        return None

    # todo I'm confused about how i'm supposed to use the session here. sessionmaker
    async def update_db(self, engine: AsyncEngine):
        async with AsyncSession(engine) as session, session.begin():
            session.add_all(self.module_item_fetch_taskpool.results())
            session.add_all(self.resource_fetch_taskpool.results())
