import asyncio
import sys
from typing import Awaitable, TypeVar, Generic, Callable

T = TypeVar("T")


class TaskPool(Generic[T]):
    """
    A TaskPool is a utility that receives submitted tasks which have an identity and which should be executed no more
    than once. It can be configured to wait for the task to finish when started, wait for the task to finish when it
    is in progress, and record the result of the task when it finishes and return it when a task with the same ID is
    submitted again.
    """

    def __init__(self, remember_result: bool = True, wait_if_in_progress: bool = True,
                 wait_if_just_started: bool = True, restart_if_finished: bool = False,
                 echo: bool = False):
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

        if not wait_if_in_progress and remember_result:
            raise ValueError("Can't remember result without waiting")

        self._results: dict[object, asyncio.Event | T | None] = {}
        self._semaphore = asyncio.Semaphore()
        self._remember_result: bool = remember_result
        self._wait_if_in_progress: bool = wait_if_in_progress
        self._wait_if_just_started: bool = wait_if_just_started
        self._restart_if_finished: bool = restart_if_finished
        self._echo = echo

    def add_values(self, results: dict[object, T]) -> None:
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
        T | None
            None, if the configuration states that we should not wait for the function to finish or not to remember the result.
            Returns the result of the function otherwise.
        """
        sem = self._semaphore
        await sem.acquire()

        if task_id in self._results.keys():
            if not self._wait_if_in_progress and isinstance(self._results[task_id], asyncio.Event):
                if self._echo: print(f"Task {task_id} in progress but configured to not wait, returning None.")
                sem.release()
                return None

            if not isinstance(self._results[task_id], asyncio.Event):
                if self._restart_if_finished:
                    if self._echo: print(
                        f"Task {task_id} already finished but configured to restart if finished, restarting.")
                    # start_task releases the semaphore, no need to do it here
                    return await self._start_task(task_id, func, **kwargs)

                if self._echo: print(f"Task {task_id} already finished, returning.")
                sem.release()
                return self._results[task_id]

            if self._echo: print(f"Task {task_id} in progress. Waiting.")

            event: asyncio.Event = self._results[task_id]
            sem.release()

            await event.wait()

            if self._echo: print(f"Finished waiting for {task_id}.")

            return self._results[task_id]
        else:
            # start_task releases the semaphore, no need to do it here
            return await self._start_task(task_id, func, **kwargs)

    async def _start_task(self, task_id: object, func, **kwargs):
        """
        Starts a task and **releases the results list semaphore**

        Parameters
        ----------
        task
            The task to start
        task_id
            The ID of the task
        event
            The event that the task is attached to

        Returns
        -------
        T
            The result of the task
        """
        sem = self._semaphore

        if self._echo: print(f"Task {task_id} started.")

        event = asyncio.Event()
        self._results[task_id] = event
        sem.release()

        if not self._wait_if_just_started:
            # noinspection PyAsyncCall
            asyncio.create_task(self._handle_task(func, task_id, event, func_args=kwargs))
            return None

        return await self._handle_task(func, task_id, event, func_args=kwargs)

    async def _handle_task(self, func: Callable, task_id: object, event: asyncio.Event, func_args : dict) -> T:
        """
        Handles the specified task

        Parameters
        ----------
        func
            The task to handle
        task_id
            The ID of the task
        event
            The event that the task is attached to

        Returns
        -------
        T
            The result of the task
        """
        sem = self._semaphore

        result = await func(**func_args)

        if isinstance(result, asyncio.Event):
            print("Result was of type asyncio.Event, this will break things!", file=sys.stderr)

        await sem.acquire()

        if self._echo: print(f"Task {task_id} finished.")

        self._results[task_id] = result if self._remember_result else None
        event.set()
        sem.release()

        return result

    async def wait_if_in_progress(self, task_id: object):
        """
        Waits for a task if it is in progress. Returns immediately otherwise.

        Parameters
        ----------
        task_id
            The task id to wait for
        """
        sem = self._semaphore

        await sem.acquire()

        if task_id in self._results and isinstance(self._results[task_id], asyncio.Event):
            event: asyncio.Event = self._results[task_id]
            sem.release()

            await event.wait()

    def clear(self) -> None:
        """
        Deletes the stored results

        Returns
        -------
        None
        """
        self._results.clear()

    def results(self) -> list[T]:
        """
        Gets the results of all currently completed tasks

        Returns
        -------
        list[T]
            The results of all currently completed tasks, excluding Nones
        """

        def filter_func(it):
            return not isinstance(it, asyncio.Event) and it is not None

        return list(filter(filter_func, self._results.values()))

    def get_completed_result(self, task_id: object) -> T | None:
        """
        Returns the result of an already completed task

        Returns
        -------
        object
            The result of the task

        Raises
        ------
        ValueError
            If the task is still in progress

        KeyError
            If the task has not been started yet or does not exist
        """
        if task_id in self._results:
            result = self._results[task_id]

            if isinstance(result, asyncio.Event):
                raise ValueError(f"{task_id} is still in progress")

            return result
        else:
            raise KeyError(f"{task_id} has not been started")

    # def get_completed_result_or_default(self, task_id: object, default : T | None = None) -> T | None:
    #     """
    #     Returns the result of an already completed task
    #
    #     Returns
    #     -------
    #     object
    #         The result of the task or the default if the task has not been started
    #
    #     Raises
    #     ------
    #     ValueError
    #         If the task is still in progress
    #     """
    #     if task_id in self._results:
    #         result = self._results[task_id]
    #
    #         if isinstance(result, asyncio.Event):
    #             raise ValueError(f"{task_id} is still in progress")
    #
    #         return result
    #     else:
    #         return default
