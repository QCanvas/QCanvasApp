import asyncio
import logging
from dataclasses import dataclass
from typing import Sequence

from bs4 import Tag, BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from qcanvas.util.linkscanner import ResourceScanner
import qcanvas.db as db
from qcanvas.util.task_pool import TaskPool

_logger = logging.getLogger()


@dataclass
class TransientResourceToPageLink:
    page_id: str
    resource_id: str

    def __hash__(self):
        return hash(self.page_id) ^ hash(self.resource_id)


async def create_module_item_resource_relations(relations: Sequence[TransientResourceToPageLink],
                                                session: AsyncSession):
    for relation in relations:
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


async def create_assignment_resource_relations(relations: Sequence[TransientResourceToPageLink],
                                               session: AsyncSession):
    for relation in relations:
        if await session.get(db.ResourceToAssignmentAssociation, (relation.page_id, relation.resource_id)) is None:
            session.add(
                db.ResourceToAssignmentAssociation(
                    assignment_id=relation.page_id,
                    resource_id=relation.resource_id
                )
            )


async def map_links_in_pages(link_scanners: Sequence[ResourceScanner], resource_pool: TaskPool[db.Resource],
                             items: Sequence[db.PageLike]) -> Sequence[TransientResourceToPageLink]:
    tasks = []

    for item in items:
        # Assignment descriptions may be null. Avoid creating extra tasks by checking here
        if item.content is None:
            continue

        tasks.append(asyncio.create_task(_extract_links_from_page(link_scanners, resource_pool, item)))

    if len(tasks) > 0:
        await asyncio.wait(tasks)

        result = []
        for task in tasks:
            result.extend(task.result())
        return result
    else:
        return []


async def _extract_links_from_page(link_scanners: Sequence[ResourceScanner], resource_pool: TaskPool[db.Resource],
                                   page: db.PageLike) -> list[TransientResourceToPageLink]:
    _logger.debug(f"Scanning %s %s for files", page.id, page.name)
    tasks = []

    for link in scan_page_for_links(page):
        tasks.append(asyncio.create_task(_process_link(link_scanners, resource_pool, link, page.course_id)))

    if len(tasks) > 0:
        await asyncio.wait(tasks)

        task_results = [task.result() for task in tasks]

        return [
            TransientResourceToPageLink(page_id=page.id, resource_id=result.id)
            for result in task_results if result is not None
        ]
    else:
        return []


def scan_page_for_links(page: db.PageLike) -> list[Tag]:
    """
    Extracts hyperlinks from a PageLike object
    """
    soup = BeautifulSoup(page.content, 'html.parser')
    return list(soup.find_all(["a", "iframe"]))


async def _process_link(link_scanners: Sequence[ResourceScanner], resource_pool: TaskPool[db.Resource], link: Tag,
                        course_id: str) -> db.Resource | None:
    for scanner in link_scanners:
        if scanner.accepts_link(link):
            resource_id = scanner.extract_id(link)

            return await resource_pool.submit(
                resource_id,
                lambda: _extract_file_info(link, scanner, resource_id, course_id)
            )

    return None


async def _extract_file_info(link: Tag, scanner: ResourceScanner, resource_id : str, course_id: str) -> db.Resource | None:
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

        result = await scanner.extract_resource(link, resource_id)
        result.id = f"{scanner.name}:{result.id}"
        result.course_id = course_id
        return result
    except BaseException as e:
        _logger.error(f"Failed to retrieve info for file id %s: %s", f"{scanner.name}:{resource_id}", str(e))
        return None
