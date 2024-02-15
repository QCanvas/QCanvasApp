from bs4 import Tag
from httpx import URL

from qcanvas import db as db
from qcanvas.net.canvas import CanvasClient
from qcanvas.util.linkscanner.resource_scanner import ResourceScanner

canvas_resource_id_prefix = "canvas_file"


class CanvasFileScanner(ResourceScanner):
    _canvas_client: CanvasClient

    def __init__(self, canvas_client: CanvasClient):
        self._canvas_client = canvas_client

    def accepts_link(self, link: Tag) -> bool:
        if link.name not in ["a", "img"]:
            return False

        return "data-api-returntype" in link.attrs.keys() and link["data-api-returntype"] == "File"

    async def extract_resource(self, link: Tag, file_id: str) -> db.Resource:
        return db.convert_legacy_file(await self._canvas_client.get_file_from_endpoint(link["data-api-endpoint"]))

    def extract_id(self, link: Tag) -> str:
        # ***REMOVED***...
        # --------------------------------- Extract this part ^^^^^^^
        return URL(link["data-api-endpoint"]).path.rsplit('/', 2)[-1]

    async def download(self):
        pass

    @property
    def name(self) -> str:
        return canvas_resource_id_prefix
