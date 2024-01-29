from typing import Union

import httpx
from gql.transport.httpx import HTTPXAsyncTransport


class CustomHTTPXAsyncTransport(HTTPXAsyncTransport):
    """:ref:`Async Transport <async_transports>` used to execute GraphQL queries
    on remote servers.

    The transport uses the httpx library with anyio.
    """

    def __init__(self, client: httpx.AsyncClient, url: Union[str, httpx.URL], **kwargs):
        super().__init__(url=url, **kwargs)
        self.client = client

    async def connect(self):
        pass

    async def close(self):
        """Do not close the client. We want to keep it."""
        pass
