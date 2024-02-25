import logging
from abc import ABC, abstractmethod
from asyncio import Lock, Event

import httpx
from httpx import URL


class AuthenticationException(Exception):
    pass


# httpx does have an authentication flow mechanism that allows you to also make other requests but I don't know if it
# will behave the same way as this does. I also finished this before I found out that existed.

class SelfAuthenticatingWithHttpClient(ABC):
    _logger = logging.getLogger(__name__)

    def __init__(self, max_retires: int = 3, client: httpx.AsyncClient = httpx.AsyncClient()):
        self.authentication_lock = Lock()
        self.client = client
        self.authentication_in_progress: Event | None = None
        self.max_retries = max_retires

    async def reauthenticate(self) -> None:
        """
        Re-authenticates the client
        """

        # Acquire the lock as to prevent multiple threads from modifying self.authentication_in_progress.
        # Not that will ever happen using asyncio alone because python async is not actually multi-processed
        await self.authentication_lock.acquire()

        # If there's no authentication already in progress
        if self.authentication_in_progress is None:
            # Update authentication_in_progress and release the lock
            self.authentication_in_progress = Event()
            self.authentication_lock.release()

            # Start the authentication
            self._logger.info(f"Authenticating {self.__class__.__name__}")
            await self._authenticate()
            self._logger.info(f"Finished authenticating {self.__class__.__name__}")
            # Update the event to unblock other coroutines
            self.authentication_in_progress.set()

            # Delete authentication_in_progress to indicate that authentication is no longer in progress
            # This lock is probably not needed (due to not actually being multi-processed) but shouldn't hurt
            await self.authentication_lock.acquire()
            self.authentication_in_progress = None
            self.authentication_lock.release()
        # Authentication is already in progress
        else:
            # Get a reference to the event
            event = self.authentication_in_progress
            # Release the lock as we are not going to access it anymore
            self.authentication_lock.release()

            # Wait for the reauthentication to finish
            self._logger.info(f"Waiting for {self.__class__.__name__}")
            await event.wait()
            self._logger.info(f"Finished waiting for {self.__class__.__name__}")

    async def do_request_and_retry_if_unauthenticated(self, url: URL, method: str, **kwargs) -> httpx.Response:
        """
        Executes a http request or reauthenticate and retries if needed
        :param url: The url of the request
        :param method: The method the request should use (post, get, etc)
        :return:
        """
        retries = 0

        async def make_request():
            return await self.client.request(url=url, method=method, **kwargs)

        # Make the initial request
        response = await make_request()

        # Retry if canvas is trying to get us to reauthenticate
        while (await self.reauthenticate_if_needed(response)) and retries < self.max_retries:
            response = await make_request()
            retries += 1

        return response

    async def reauthenticate_if_needed(self, response: httpx.Response) -> bool:
        """
        Inspects a response and activates reauthentication if the response indicates we need to
        :param response: The response to inspect
        :return: True if reauthentication was activated, false if not
        """

        if self.detect_authentication_needed(response):
            await self.reauthenticate()
            return True

        return False

    @abstractmethod
    def detect_authentication_needed(self, response: httpx.Response) -> bool:
        ...

    @abstractmethod
    async def _authenticate(self) -> None:
        """
        Authenticates the client
        """
        ...
