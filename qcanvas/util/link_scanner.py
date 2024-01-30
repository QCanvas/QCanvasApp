from bs4 import Tag
from httpx import URL

import qcanvas.db as db
from qcanvas.net.canvas import CanvasClient


class LinkedResourceHandler:
    def accepts_link(self, link: Tag) -> bool:
        raise NotImplementedError()

    async def extract_resource(self, link: Tag) -> db.Resource:
        raise NotImplementedError()

    def extract_id(self, link: Tag) -> str:
        raise NotImplementedError()

    async def download(self):
        raise NotImplementedError()


class CanvasLinkedResourceHandler(LinkedResourceHandler):
    _canvas_client: CanvasClient

    def __init__(self, canvas_client: CanvasClient):
        self._canvas_client = canvas_client

    def accepts_link(self, link: Tag) -> bool:
        return "data-api-returntype" in link.attrs.keys() and link["data-api-returntype"] == "File"

    async def extract_resource(self, link: Tag) -> db.Resource:
        return db.convert_legacy_file(await self._canvas_client.get_file_from_endpoint(link["data-api-endpoint"]))

    def extract_id(self, link: Tag) -> str:
        return "canvas_" + URL(link["data-api-endpoint"]).path.rsplit('/', 2)[-1]

    async def download(self):
        pass
