import asyncio
import json
import logging

import gql
import httpx
from gql.transport.exceptions import TransportQueryError
from httpx import URL, Response
from tenacity import retry, wait_exponential, wait_random, retry_if_exception, stop_after_attempt, wait_fixed, \
    retry_if_exception_type

from qcanvas.net.custom_httpx_async_transport import CustomHTTPXAsyncTransport
from qcanvas.net.self_authenticating import SelfAuthenticating, AuthenticationException

from qcanvas.net.canvas.legacy_canvas_types import LegacyFile, LegacyPage

class RatelimitedException(Exception):
    def __init__(self):
        super().__init__("Canvas is ratelimiting me yay")


class CanvasClient(SelfAuthenticating):
    _logger = logging.getLogger(__name__)
    _net_op_sem = asyncio.Semaphore(20)

    @staticmethod
    async def verify_config(canvas_url: URL, api_key: str) -> bool:
        """
        Makes a request to canvas to verify that the url and key are correct.
        :param canvas_url: The canvas url to verify
        :param api_key: The api key to verify
        :return: True if everything looks ok, false if the api key or url is wrong
        """
        client = httpx.AsyncClient()
        # Make a request to an endpoint that returns very little/no data (for students at least) to check if everything
        # is working
        response = await client.get(url=canvas_url.join("api/v1/accounts"),
                                    headers={"Authorization": f"Bearer {api_key}"})

        return response.is_success

    def __init__(self, canvas_url: URL, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.canvas_url = canvas_url
        self.client = httpx.AsyncClient(timeout=60)
        self.max_retries = 1
        self.client.headers["Authorization"] = f"Bearer {self.api_key}"

    @retry(
        wait=wait_exponential(exp_base=1.2, max=10) + wait_random(0, 1),
        retry=retry_if_exception_type(RatelimitedException),
        stop=stop_after_attempt(8)
    )
    async def get_courses(self):
        with self._net_op_sem:
            return await self.client.get(self.canvas_url.join("api/v1/courses"))

    @retry(
        wait=wait_exponential(exp_base=1.2, max=10) + wait_random(0, 1),
        retry=retry_if_exception_type(RatelimitedException),
        stop=stop_after_attempt(8)
    )
    async def get_page(self, page_id: str | int, course_id: str | int) -> LegacyPage:
        async with self._net_op_sem:
            response = self.detect_ratelimit_and_raise(await self.client.get(self.canvas_url.join(f"api/v1/courses/{course_id}/pages/{page_id}")))

            return LegacyPage.from_dict(json.loads(response.text))

    @retry(
        wait=wait_exponential(exp_base=1.2, max=10) + wait_random(0, 1),
        retry=retry_if_exception_type(RatelimitedException),
        stop=stop_after_attempt(8)
    )
    async def get_file(self, file_id: str | int, course_id: str | int) -> LegacyFile:
        async with self._net_op_sem:
            response = self.detect_ratelimit_and_raise(await self.client.get(self.canvas_url.join(f"api/v1/courses/{course_id}/files/{file_id}")))

            response.raise_for_status()

            return LegacyFile.from_dict(json.loads(response.text))

    @retry(
        wait=wait_exponential(exp_base=1.2, max=10) + wait_random(0, 1),
        retry=retry_if_exception_type(RatelimitedException),
        stop=stop_after_attempt(8)
    )
    async def get_file_from_endpoint(self, endpoint_url : str) -> LegacyFile:
        async with self._net_op_sem:
            response = self.detect_ratelimit_and_raise(await self.client.get(endpoint_url))

            response.raise_for_status()

            return LegacyFile.from_dict(json.loads(response.text))

    def detect_ratelimit_and_raise(self, response: Response) -> Response:
        # Who the FUCK decided to use 403 instead of 429?? With this stupid message??
        # Fuck you instructure, learn to code
        # And the newline at the end for some fucking reason is the cherry on top...
        if response.status_code == 403 and response.text == "403 Forbidden (Rate Limit Exceeded)\n":
            raise RatelimitedException()

        return response

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(5) + wait_random(0, 1),
        retry=retry_if_exception_type(TransportQueryError)
    )
    async def do_graphql_query(self, query: gql.client.DocumentNode, **kwargs):
        """
        Executes a graphql query and reauthenticates the client if needed
        :param query:
        :param operation: The operation to execute
        :return: The result
        """
        async with self._net_op_sem:
            gql_transport = CustomHTTPXAsyncTransport(self.client, self.canvas_url.join("api/graphql"))
            gql_client = gql.Client(transport=gql_transport, execute_timeout=60)

            return await gql_client.execute_async(query, variable_values=kwargs)

    async def do_request_and_retry_if_unauthenticated(self, url: URL):
        """
        Executes a http request or reauthenticate and retries if needed
        :param url: The url of the request
        :return:
        """
        retries = 0

        # Make the initial request
        response = await self.client.get(url)

        # Retry if canvas is trying to get us to reauthenticate
        while (await self.reauthenticate_if_needed(response)) and retries < self.max_retries:
            response = await self.client.get(url)
            retries += 1

        return response.text

    async def reauthenticate_if_needed(self, response: Response):
        """
        Inspects a response and activates reauthentication if the response indicates we need to
        :param response: The response to inspect
        :return: True if reauthentication was activated, false if not
        """

        if self.detect_authentication_needed(response):
            await self.reauthenticate()
            return True

        return False

    def detect_authentication_needed(self, response: Response):
        """
        Detects if a response is redirecting us to the login page or is giving us a 401 (unauthorised)
        :param response: The response to check
        :return: True if reauthentication is needed
        """
        return response.url.path == "/login/canvas" or response.status_code == 401

    async def _authenticate(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        token_response = await self.client.get(self.canvas_url.join("login/session_token"), headers=headers)

        if token_response.is_success:
            session_url = json.loads(token_response.text)["session_url"]
            self._logger.debug("Got token response for authentication")

            if session_url is not None:
                req = await self.client.get(session_url)
                if req.status_code != 302:
                    self._logger.error("Error when activating session from request")
                    raise AuthenticationException("Authentication was not successful")
            else:
                raise AuthenticationException("Token response body was malformed")
        else:
            self._logger.error("Authentication failed, API key may be invalid")
            raise AuthenticationException("Authentication failed, check your API key")
