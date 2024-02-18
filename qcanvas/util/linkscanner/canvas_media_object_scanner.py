import json
from typing import Any

from bs4 import Tag, BeautifulSoup
from httpx import URL, AsyncClient

from qcanvas import db as db
from qcanvas.util.linkscanner import ResourceScanner


class CanvasMediaObjectScanner(ResourceScanner):

    def __init__(self, client : AsyncClient):
        self.client = client

    @property
    def name(self) -> str:
        return "canvas_media_object"

    def accepts_link(self, link: Tag) -> bool:
        return (
                link.name == "iframe"
                and "data-media-type" in link.attrs.keys()
                and link.attrs["data-media-type"] == "video"
        )

    async def extract_resource(self, link: Tag, file_id: str) -> db.Resource:
        # Get the page for the embedded player (I could not find another way to get the needed data from canvas)
        response = (await self.client.get(link.attrs["src"])).text
        # Parse the HTML response
        doc = BeautifulSoup(response, "html.parser")
        media_data: None | dict[str, Any] = None

        # Find all script tags (one of them has the data we are interested in)
        for script_tag in doc.find_all("script", {}):
            body = script_tag.text.strip()

            # If the tag content starts with this then it has the data we want
            if "INST = {" in body:
                # Find the data that we are interested in (is on a line that starts with "ENV = ")
                line: str = next(filter(lambda x: x.strip().startswith("ENV ="), script_tag.text.splitlines()))
                # Parse the json embedded in the script tag
                media_data = json.loads(line.lstrip("ENV = ").rstrip(";"))["media_object"]
                break

        if media_data is None:
            raise Exception("Could not extract media info")

        # The highest quality stream is the first
        media_source = media_data["media_sources"][0]

        return db.Resource(
            id=file_id,
            url=media_source["src"],
            file_name=media_data["title"],
            file_size=int(media_source["size"]) * 1024  # Seems to be recorded in KiB, not bytes
        )

    def extract_id(self, link: Tag) -> str:
        return link.attrs["data-media-id"]