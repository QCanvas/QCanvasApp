import json
import logging
from urllib.parse import unquote

import gql
import httpx
from gql.transport.exceptions import TransportQueryError
from httpx import URL, Response

from qcanvas.net.custom_httpx_async_transport import CustomHTTPXAsyncTransport
from qcanvas.net.self_authenticating import SelfAuthenticating, AuthenticationException


class CanvasClient(SelfAuthenticating):
    _logger = logging.getLogger(__name__)

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
        self.max_retries = 3

    async def get_courses(self):
        return await self.do_request_and_retry_if_unauthenticated(self.canvas_url.join("api/v1/courses"))

    async def do_graphql_query(self, query: gql.client.DocumentNode, **kwargs):
        """
        Executes a graphql query and reauthenticates the client if needed
        :param query:
        :param operation: The operation to execute
        :return: The result
        """

        retries = 0

        while retries < self.max_retries:
            try:
                if "_csrf_token" in self.client.cookies:
                    # If we have the csrf token then we should be right to make the request

                    gql_transport = CustomHTTPXAsyncTransport(self.client, self.canvas_url.join("api/graphql"))
                    gql_client = gql.Client(transport=gql_transport)

                    return await gql_client.execute_async(query, variable_values=kwargs, extra_args={
                        "headers": {
                            "X-CSRF-Token": unquote(self.client.cookies["_csrf_token"]),  # Un-percent-encode the token
                        }
                    })
                else:
                    # Otherwise reauthenticate ourselves
                    await self.reauthenticate()
                    retries += 1
            except TransportQueryError as err:
                # If an error occurred, try reauthenticating
                print(err)

                if retries >= self.max_retries:
                    raise err
                else:
                    await self.reauthenticate()
                    retries += 1

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
