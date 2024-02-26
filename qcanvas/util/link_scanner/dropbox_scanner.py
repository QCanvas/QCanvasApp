import httpx
from bs4 import Tag
from httpx import URL

from qcanvas import db as db
from qcanvas.util.link_scanner import ResourceScanner


# from httpx import URL


def parse_content_disposition(header: str) -> dict[str, str | None]:
    bad_chars = "\" \t"
    result = {}

    for statement in header.split(";"):
        split = statement.split("=", 2)

        result[split[0].strip(bad_chars)] = None if len(split) == 1 else split[1].strip(bad_chars)

    return result


class DropboxScanner(ResourceScanner):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    def accepts_link(self, link: Tag) -> bool:
        if link.name != "a":
            return False

        if "href" in link.attrs:
            url = URL(link.attrs["href"])

            return url.host == "www.dropbox.com" and url.path.split("/", 2)[1] == "s"
        else:
            return False

    async def extract_resource(self, link: Tag, file_id: str) -> db.Resource:
        url = URL(link.attrs["href"]).copy_set_param("dl", 1)

        req = self.client.build_request(
            method="GET",
            url=url
        )

        # The following code essentially starts downloading the file, reads the headers and then stops downloading it,
        # just to ge the size of the file
        resp = await self.client.send(req, follow_redirects=True, stream=True)

        try:
            resp.raise_for_status()

            filename = parse_content_disposition(resp.headers["content-disposition"])["filename"]
            size = int(resp.headers["content-length"])

            return db.Resource(id=file_id, url=str(url), file_name=filename, file_size=size)
        finally:
            await resp.aclose()

    def extract_id(self, link: Tag) -> str:
        # ***REMOVED***
        # ------- Extract this part ^^^^^^^^^^^^^^^
        return URL(link.attrs["href"]).path.split("/", 3)[2]

    @property
    def name(self) -> str:
        return "dropbox"
