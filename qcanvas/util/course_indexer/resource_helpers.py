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

resource_elements = ["a", "iframe", "img"]


# todo could probably just use the database types directly now
@dataclass
class TransientResourceToPageLink:
    """
    Represents a temporary link between a page and a resource that will be added to the database soon.
    """
    page_id: str
    resource_id: str

    def __hash__(self):
        return hash(self.page_id) ^ hash(self.resource_id)


async def create_module_item_resource_relations(relations: Sequence[TransientResourceToPageLink],
                                                session: AsyncSession):
    """
    Creates a link between module items/pages and resources found on those pages
    """
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


async def create_assignment_resource_relations(relations: Sequence[TransientResourceToPageLink], session: AsyncSession):
    """
    Turns temporary TransientResourceToPageLink into a persistent relation in the database
    """
    for relation in relations:
        if await session.get(db.ResourceToAssignmentAssociation, (relation.page_id, relation.resource_id)) is None:
            session.add(
                db.ResourceToAssignmentAssociation(
                    assignment_id=relation.page_id,
                    resource_id=relation.resource_id
                )
            )


async def map_resources_in_pages(link_scanners: Sequence[ResourceScanner], resource_pool: TaskPool[db.Resource],
                                 items: Sequence[db.PageLike]) -> list[TransientResourceToPageLink]:
    """
    Produce a list of resource to page links from resources extracted from the specified `items` using `link_scanners`.
    Extracted resources will be added to `resource_pool`
    """
    tasks = []

    for item in items:
        # Assignment descriptions may be null. Avoid creating extra tasks by checking here
        if item.content is None:
            continue

        # extract resources from the page
        tasks.append(asyncio.create_task(_extract_resources_from_page(link_scanners, resource_pool, item)))

    if len(tasks) > 0:
        # Wait for all tasks to complete
        await asyncio.wait(tasks)

        result = []
        # Flatten the array of results
        for task in tasks:
            result.extend(task.result())

        return result
    else:
        return []


async def _extract_resources_from_page(link_scanners: Sequence[ResourceScanner], resource_pool: TaskPool[db.Resource],
                                       page: db.PageLike) -> list[TransientResourceToPageLink]:
    """
    Extracts any detected resource links from the specified page and then uses `link_scanners` to extract information
    about which is then added to the `resource_pool`.

    Returns
    -------
    list
        A list of resource to page links for any resources found on this page.
    """
    _logger.debug(f"Scanning %s %s for files", page.id, page.name)
    tasks = []

    # Extract iframes, hyperlinks, etc from the page
    for link in _scan_page_for_links(page):
        tasks.append(asyncio.create_task(_process_link(link_scanners, resource_pool, link, page.course_id)))

    if len(tasks) > 0:
        # Wait for all tasks to complete
        await asyncio.wait(tasks)

        task_results = [task.result() for task in tasks]

        # Convert every non-null result in the task results to a resource page link and return it
        return [
            TransientResourceToPageLink(page_id=page.id, resource_id=result.id)
            for result in task_results if result is not None
        ]
    else:
        return []


def _scan_page_for_links(page: db.PageLike) -> list[Tag]:
    """
    Extracts (potential) resource elements from a PageLike object
    """
    soup = BeautifulSoup(page.content, 'html.parser')
    return list(soup.find_all(resource_elements))


async def _process_link(link_scanners: Sequence[ResourceScanner], resource_pool: TaskPool[db.Resource], link: Tag,
                        course_id: str) -> db.Resource | None:
    """
    Iterates over `link_scanners` to find one that will accept `link`, then uses it to fetch resource information and
     adds it to the `resource_pool`.
    If no scanner accepts the link then None is returned.
    """
    for scanner in link_scanners:
        if scanner.accepts_link(link):
            resource_id = scanner.extract_id(link)

            return await resource_pool.submit(
                f"{scanner.name}:{resource_id}",  # match the format used by the resource id
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
        result.id = f"{scanner.name}:{result.id}"  # Prefix the scanner name to prevent resources from different sites potentially clashing
        result.course_id = course_id
        return result
    except BaseException as e:
        _logger.error(f"Failed to retrieve info for file id %s: %s", f"{scanner.name}:{resource_id}", str(e))
        return None
