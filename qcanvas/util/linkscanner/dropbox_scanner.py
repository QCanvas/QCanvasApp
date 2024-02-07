import httpx
from bs4 import Tag
from httpx import URL

# from httpx import URL

from qcanvas import db as db
from qcanvas.util.linkscanner import ResourceScanner


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
        if "href" in link.attrs:
            url = URL(link.attrs["href"])

            return url.host == "www.dropbox.com" and url.path.split("/", 2)[1] == "s"
        else:
            return False

    async def extract_resource(self, link: Tag) -> db.Resource:
        url = URL(link.attrs["href"]).copy_set_param("dl", 1)
        id = self._id_helper(url)

        req = self.client.build_request(
            method="GET",
            url=url
        )

        resp = await self.client.send(req, follow_redirects=True, stream=True)

        try:
            resp.raise_for_status()

            filename = parse_content_disposition(resp.headers["content-disposition"])["filename"]
            size = int(resp.headers["content-length"])

            return db.Resource(id, str(url), filename, id, file_size=size)
        finally:
            await resp.aclose()

    def extract_id(self, link: Tag) -> str:
        return self._id_helper(URL(link.attrs["href"]))

    def _id_helper(self, url : URL) -> str:
        return "dropbox_" + url.path.split("/", 3)[2]

    async def download(self):
        pass
