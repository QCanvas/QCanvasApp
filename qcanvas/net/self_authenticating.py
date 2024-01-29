import logging
from asyncio import Lock, Event


class AuthenticationException(Exception):
    pass

# httpx does have an authentication flow mechanism that allows you to also make other requests but I don't know if it
# will behave the same way as this does. I also finished this before I found out that existed.

class SelfAuthenticating:
    _logger = logging.getLogger(__name__)

    def __init__(self):
        self.authentication_lock = Lock()
        self.authentication_in_progress: Event | None = None

    async def reauthenticate(self):
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

    async def _authenticate(self) -> None:
        """
        Authenticates the client
        """
        raise NotImplemented
