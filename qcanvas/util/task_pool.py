import asyncio
import sys
from typing import Awaitable, TypeVar, Generic

T = TypeVar("T")


class TaskPool(Generic[T]):
    """
    A TaskPool is a utility that receives submitted tasks which have an identity and which should be executed no more
    than once. It can be configured to wait for the task to finish when started, wait for the task to finish when it
    is in progress, and record the result of the task when it finishes and return it when a task with the same ID is
    submitted again.
    """

    _results: dict[object, asyncio.Event | T | None]
    _semaphore = asyncio.Semaphore()

    _remember_result: bool
    _wait_if_in_progress: bool
    _wait_if_just_started: bool
    _echo: bool

    def __init__(self, remember_result: bool = True, wait_if_in_progress: bool = True,
                 wait_if_just_started: bool = True, echo: bool = False):
        """
        Parameters
        ----------
        remember_result : bool
            Whether to store the result of submitted tasks

        wait_if_just_started : bool
            Whether to await a newly started task or return immediately

        wait_if_in_progress : bool
            Whether to await a task that is in progress or return immediately

        echo : bool
            Whether to print the status of tasks as they are awaited and submitted
        """
        super().__init__()

        if not wait_if_in_progress and remember_result:
            raise ValueError("Can't remember result without waiting")

        self._remember_result = remember_result
        self._wait_if_in_progress = wait_if_in_progress
        self._wait_if_just_started = wait_if_just_started
        self._echo = echo
        self._results = {}

    def add_completed_values(self, results: dict[object, T]) -> None:
        """
        Adds the specified values from the dictionary as stored results.

        Parameters
        ----------
        results
            The results to store, where the key is the ID and the value is the result

        Returns
        -------
            None
        """
        self._results.update(**results)

    async def submit(self, task_id: object, func, **kwargs) -> T | None:
        """
        Submits a task and executes it. Depending on configuration, waits for it and returns the result of it.

        Parameters
        ----------
        task_id: object
            The identity of the task. E.g. "task_get_file_1" or "task_get_file_2"

        func : lambda
            The function to execute.
            Should be provided in the form of a lambda which executes some async function without using the await keyword.
            E.g::
                # Right
                taskpool.submit(..., func=lambda: some_async_function(some_val))
                # Wrong
                taskpool.submit(..., func=lambda: async some_async_function(some_val))
                #                                 ^^^^^
        kwargs
            Extra arguments for the lambda
        Returns
        -------
        None, if the configuration states that we should not wait for the function to finish or not to remember the result.
        The result of the function otherwise.
        """
        sem = self._semaphore
        await sem.acquire()

        if task_id in self._results.keys():
            if not self._wait_if_in_progress:
                if self._echo: print(f"Task {task_id} in progress or finished. Configured to not wait.")
                sem.release()
                return None

            if not isinstance(self._results[task_id], asyncio.Event):
                if self._echo: print(f"Task {task_id} already finished, returning.")
                sem.release()
                return self._results[task_id]

            if self._echo: print(f"Task {task_id} in progress. Waiting.")

            event: asyncio.Event = self._results[task_id]
            sem.release()

            await event.wait()

            if self._echo: print(f"Task {task_id} finished.")

            return self._results[task_id]
        else:
            if self._echo: print(f"Task {task_id} started - Origin.")

            event = asyncio.Event()
            self._results[task_id] = event
            sem.release()

            if not self._wait_if_just_started:
                # noinspection PyAsyncCall
                asyncio.create_task(self._handle_task(func(**kwargs), task_id, event))
                return None

            return await self._handle_task(func(**kwargs), task_id, event)

    async def _handle_task(self, task: Awaitable[object], task_id: object, event: asyncio.Event) -> T:
        """
        Handles the specified task

        Parameters
        ----------
        task
            The task to handle
        task_id
            The ID of the task
        event
            The event that the task is attached to

        Returns
        -------
            The result of the task
        """
        sem = self._semaphore

        result = await task

        if isinstance(result, asyncio.Event):
            print("Result was of type asyncio.Event, this will break things!", file=sys.stderr)

        await sem.acquire()

        if self._echo: print(f"Task {task_id} finished - Origin.")

        self._results[task_id] = result if self._remember_result else None
        event.set()
        sem.release()

        return result

    def clear(self) -> None:
        """
        Deletes the stored results

        Returns
        -------
            None
        """
        self._results.clear()

    def results(self) -> list[T | None]:
        def filter_func(it):
            return not isinstance(it, asyncio.Event) and it is not None

        return list(filter(filter_func, self._results.values()))
