from typing import Union, Optional, Dict, Any

import httpx
from gql.transport.httpx import HTTPXAsyncTransport
from graphql import DocumentNode


class CustomHTTPXAsyncTransport(HTTPXAsyncTransport):
    """:ref:`Async Transport <async_transports>` used to execute GraphQL queries
    on remote servers.

    The transport uses the httpx library with anyio.
    """

    def __init__(self, client: httpx.AsyncClient, url: Union[str, httpx.URL], headers: dict[str, Any] | None = None, **kwargs):
        super().__init__(url=url, **kwargs)
        self.client = client
        self.headers = headers or {}

    async def connect(self):
        pass

    async def close(self):
        """Do not close the client. We want to keep it."""
        pass

    def _prepare_request(self, document: DocumentNode, variable_values: Optional[Dict[str, Any]] = None,
                         operation_name: Optional[str] = None, extra_args: Optional[Dict[str, Any]] = None,
                         upload_files: bool = False) -> Dict[str, Any]:
        result = super()._prepare_request(document, variable_values, operation_name, extra_args, upload_files)
        result["headers"] = self.headers

        return result


