from abc import ABC, abstractmethod

from bs4 import Tag

import qcanvas.db as db


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

    @abstractmethod
    async def download(self):
        ...


