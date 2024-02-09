from abc import ABC, abstractmethod

from bs4 import Tag

import qcanvas.db as db


class ResourceScanner(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def accepts_link(self, link: Tag) -> bool:
        ...

    @abstractmethod
    async def extract_resource(self, link: Tag, file_id : str) -> db.Resource:
        ...

    @abstractmethod
    def extract_id(self, link: Tag) -> str:
        ...

    @abstractmethod
    async def download(self):
        ...


