import asyncio
from abc import ABC, abstractmethod
from typing import AsyncIterator

import httpx
from bs4 import Tag

import qcanvas.db as db
from qcanvas.util import download_pool


class ResourceScanner(ABC):
    """
    A resource scanner extracts resources from canvas pages.
    The resource may be an embedded video, a file or anything that will be of use to the user.
    Each scanner should be responsible for only 1 type of resource.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the resource scanner.
        Will be attached to the resource id externally.
        """
        ...

    @abstractmethod
    def accepts_link(self, link: Tag) -> bool:
        """
        Whether this resource scanner accepts the specified link
        """
        ...

    @abstractmethod
    async def extract_resource(self, link: Tag, file_id: str) -> db.Resource:
        """
        Extract information about the resource in the specified tag
        Parameters
        ----------
        link
            The element that links to the resource
        file_id
            The id of the file (as produced from `extract_id`)
        Returns
        -------
            The resource
        """
        ...

    @abstractmethod
    def extract_id(self, link: Tag) -> str:
        """
        Extracts a unique id from a file link
        """
        ...

    async def download(self, resource: db.Resource) -> AsyncIterator[int]:
        yield 0

        download_destination = resource.download_location
        download_destination.parent.mkdir(parents=True, exist_ok=True)

        with open(download_destination, "wb") as file:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                async with client.stream(method='get', url=resource.url) as resp:
                    resp.raise_for_status()

                    async for chunk in resp.aiter_bytes():
                        file.write(chunk)
                        yield resp.num_bytes_downloaded

