import asyncio
import logging
import sys
import traceback
from asyncio import Task
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from gql import gql
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker, AsyncSession
from sqlalchemy.orm import selectin_polymorphic, selectinload

import qcanvas.db as db
import qcanvas.queries as queries
from qcanvas.net.canvas import CanvasClient
from qcanvas.util.download_pool import DownloadPool
from qcanvas.util.linkscanner.resource_scanner import ResourceScanner
from qcanvas.util.task_pool import TaskPool

import qcanvas.util.course_indexer.conversion_helpers as conv_helper
import qcanvas.util.course_indexer.resource_helpers as resource_helper

from qcanvas.util.linkscanner.canvas_link_scanner import canvas_resource_id_prefix

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
            for item_position, g_module_item in enumerate(g_module.module_items):
                content = g_module_item.content

                if isinstance(content, queries.Page) or isinstance(content, queries.File):
                    # todo need to decide how to only rescan old pages or only rescan new pages without fetching content of old pages again for no good reason
                    if (
                            content.m_id not in pages_id_mapped
                            or content.updated_at.replace(tzinfo=None) > pages_id_mapped[content.m_id].updated_at
                    ):
                        result.append(TransientModulePage(content, g_course.m_id, g_module.q_id, item_position))
                    else:
                        _logger.debug("Page %s is already up to date", content.m_id)

    return result

# todo make this reusable and add some way of refreshing only a list of pages or one page or one course or something
# todo use logger instead of print and put some signals around the place for useful things, e.g. indexing progress
class DataManager:
    def __init__(self,
                 client: CanvasClient,
                 sessionmaker: AsyncSessionMaker,
                 link_scanners: Sequence[ResourceScanner],
                 last_update: datetime):

        self._client = client
        self._link_scanners = link_scanners
        self._session_maker = sessionmaker
        self._last_update = last_update

        self._resource_pool = TaskPool[db.Resource]()
        self._moduleitem_pool = TaskPool[db.ModuleItem]()
        self.download_pool = DownloadPool()

        # Map all the scanners we have to their own name
        self._scanner_name_map = {scanner.name: scanner for scanner in self._link_scanners}

        self._init_called = False

    async def init(self):
        self._init_called = True

        async with self._session_maker.begin() as session:
            # Load existing pages and resources from the database
            existing_pages = (await session.execute(
                select(db.ModuleItem)
                .options(selectin_polymorphic(db.ModuleItem, [db.ModulePage]))
            )).scalars().all()

            existing_resources = (await session.execute(
                select(db.Resource)
            )).scalars().all()

            # Add the existing items to the relevant taskpools
            self._add_resources_and_pages_to_taskpool(existing_pages=existing_pages,
                                                      existing_resources=existing_resources)

    async def _download_resource_helper(self, link_handler : ResourceScanner, resource: db.Resource):
        try:
            async for progress in link_handler.download(resource):
                yield progress

            # Do this here because this function will only be called once for this resource
            async with self._session_maker.begin() as session:
                session.add(resource)
                resource.state = db.ResourceState.DOWNLOADED
        except BaseException as e:
            async with self._session_maker.begin() as session:
                session.add(resource)
                resource.state = db.ResourceState.FAILED
                resource.fail_message = str(e)

            raise e

    async def download_resource(self, resource: db.Resource):
        if not self._init_called:
            sys.stderr.write("WARNING! INIT NOT CALLED FOR COURSE LOADER!! YOU'VE FUCKED UP!!!!!!!!!!!")

        scanner_name: str = resource.id.split(':', 2)[0]
        # Find the scanner that will deal with this resource
        scanner = self._scanner_name_map[scanner_name]

        await self.download_pool.submit(resource.id, lambda: self._download_resource_helper(scanner, resource))

    async def update_item(self, item: db.Base):
        async with self._session_maker.begin() as session:
            await session.merge(item)

    async def get_data(self):
        """
        Loads all the course data
        """
        async with self._session_maker.begin() as session:
            module_items_load = selectinload(db.Course.modules).joinedload(db.Module.items)

            # Eagerly load fucking everything
            options = [
                selectinload(db.Course.modules)
                .joinedload(db.Module.course),

                module_items_load.selectin_polymorphic([db.ModulePage, db.ModuleFile])
                .joinedload(db.ModuleItem.module),

                module_items_load.joinedload(db.ModuleItem.resources),
                selectinload(db.Course.assignments)
                .joinedload(db.Assignment.course),

                selectinload(db.Course.assignments)
                .joinedload(db.Assignment.resources),

                selectinload(db.Course.term),

                selectinload(db.Course.module_items)
                .joinedload(db.ModuleItem.course),

                selectinload(db.Course.preferences)
                .joinedload(db.CoursePreferences.course),

                selectinload(db.Course.resources)
                .joinedload(db.Resource.course)
            ]

            return (await session.execute(select(db.Course).options(*options))).scalars().all()

    async def synchronize_with_canvas(self):
        print("Querying index")
        raw_query = (await self._client.do_graphql_query(gql(queries.all_courses.DEFINITION), detailed=True))
        print("Loading data")
        await self.load_courses_data(queries.AllCoursesQueryData(**raw_query).all_courses)

    async def load_courses_data(self, g_courses: Sequence[queries.Course]):
        if not self._init_called:
            sys.stderr.write("WARNING! INIT NOT CALLED FOR COURSE LOADER!! YOU'VE FUCKED UP!!!!!!!!!!!")

        """
        Loads data for all specified courses, including loading module pages and scanning for resources.
        """
        # if self._operation_semaphore.locked():
        #     raise Exception("Only 1 sync operation may happen at once")

        # async with self._operation_semaphore:

        async with self._session_maker.begin() as session:
            # Load module pages/files for the courses
            await self._load_module_items(g_courses, session)

            # Collect assignments from the courses
            assignments = []

            for g_course in g_courses:
                # Create needed data in the session
                term = await conv_helper.create_term(g_course, session)
                await conv_helper.create_course(g_course, session, term)
                await conv_helper.create_modules(g_course, session)

                # Add the course assignments to the list
                assignments.extend(await conv_helper.create_assignments(g_course, session))

            # Scan assignments for resources
            await self._scan_assignments_for_resources(assignments, session)

            # Add all resources back into the session
            session.add_all(self._resource_pool.results())

    async def _scan_assignments_for_resources(self, assignments, session):
        """
        Scans assignments for resources
        """
        print("Scanning assignments for resources")

        await resource_helper.create_assignment_resource_relations(
            await resource_helper.map_resources_in_pages(
                link_scanners=self._link_scanners,
                resource_pool=self._resource_pool,
                items=assignments
            ),
            session
        )

    async def _load_module_items(self, g_courses: Sequence[queries.Course], session: AsyncSession):
        # Get the ids of all the courses we are going to index/load
        course_ids = [g_course.m_id for g_course in g_courses]

        # Prepare pages for loading
        existing_pages = (
            await session.execute(
                select(db.ModulePage)
                .where(db.ModuleItem.course_id.in_(course_ids))
            )).scalars().all()
        pages_to_update = _prepare_out_of_date_pages_for_loading(g_courses, existing_pages)
        module_items = await self._load_page_content(pages_to_update)

        print("Scanning pages for resources")
        await resource_helper.create_module_item_resource_relations(
            await resource_helper.map_resources_in_pages(
                link_scanners=self._link_scanners,
                resource_pool=self._resource_pool,
                items=list(filter(lambda x: isinstance(x, db.PageLike), module_items))
            ),
            session
        )

        session.add_all(module_items)

    def _add_resources_and_pages_to_taskpool(self, existing_pages: Sequence[db.ModuleItem],
                                             existing_resources: Sequence[db.Resource]):
        self._moduleitem_pool.add_values({page.id: page for page in existing_pages})
        self._resource_pool.add_values({resource.id: resource for resource in existing_resources})
        # Add downloaded resources to the resource pool so we don't download them again
        self.download_pool.add_values({resource.id: None for resource in existing_resources if resource.state == db.ResourceState.DOWNLOADED})

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
                task = asyncio.create_task(self._load_module_file(content, page.course_id, page.module_id, page.position))
                tasks.append(task)
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
        """
        Fetches resource information for the module file and converts it into a module item
        """
        _logger.debug(f"Loading module file %s %s", g_file.m_id, g_file.display_name)

        resource = await self._resource_pool.submit(
            f"{canvas_resource_id_prefix}:{g_file.m_id}",  # to match the format used by canvas link extractor
            lambda: self._fetch_module_file_resource(g_file, course_id)
        )

        return await self._moduleitem_pool.submit(
            g_file.m_id,
            lambda: self._fetch_module_file_page(g_file, resource, course_id, module_id, position)
        )

    async def _fetch_module_file_resource(self, file: queries.File, course_id: str) -> db.Resource:
        """
        Fetches information about the specified file from canvas
        """
        _logger.debug(f"Fetching file (for module file) %s %s", file.m_id, file.display_name)
        result = await self._client.get_file(file.m_id, course_id)
        resource = db.convert_file(file, result.size)
        resource.id = f"{canvas_resource_id_prefix}:{resource.id}"
        resource.course_id = course_id

        return resource

    async def load_module_page(self, g_page: queries.Page, course_id: str, module_id: str,
                               position: int) -> db.ModulePage | None:
        """
        Creates task for loading the specified module page
        """
        return await self._moduleitem_pool.submit(
            g_page.m_id,
            lambda: self._fetch_module_item_page(g_page, course_id, module_id, position)
        )

    async def _fetch_module_item_page(self, page: queries.Page, course_id: str, module_id: str,
                                      position: int) -> db.ModulePage | None:
        """
        Fetches module page content from canvas. Returns None if the page could not be loaded.
        """
        _logger.debug("Fetching module page %s %s", page.m_id, page.title)

        try:
            # Get the page
            result = await self._client.get_page(page.m_id, course_id)
        except BaseException as e:
            # Handle any errors
            _logger.error(e)
            traceback.print_exc()
            return None

        if result.locked_for_user:
            _logger.error("Page %s %s is locked", page.m_id, page.title)
            return None

        page = db.convert_page(page, result.body)
        page.module_id = module_id
        page.course_id = course_id
        page.position = position

        return page

    @staticmethod
    async def _fetch_module_file_page(file: queries.File, resource: db.Resource, course_id: str,
                                      module_id: str, position: int) -> db.ModuleFile:
        """
        Converts module file information into the database format
        """
        _logger.debug(f"Creating page for module file %s %s", file.m_id, file.display_name)

        page = db.convert_file_page(file)
        page.module_id = module_id
        page.course_id = course_id
        page.position = position
        page.resources.append(resource)

        return page

    @property
    def link_scanners(self):
        return self._link_scanners
