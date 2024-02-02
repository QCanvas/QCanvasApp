from bs4 import Tag

import qcanvas.db as db


class LinkedResourceHandler:
    def accepts_link(self, link: Tag) -> bool:
        raise NotImplementedError()

    async def extract_resource(self, link: Tag) -> db.Resource:
        raise NotImplementedError()

    def extract_id(self, link: Tag) -> str:
        raise NotImplementedError()

    async def download(self):
        raise NotImplementedError()


