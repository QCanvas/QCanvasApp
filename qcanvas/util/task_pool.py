import asyncio
import logging
from typing import TypeVar, Generic, Any

from qcanvas.util.in_progress_task import InProgressTask

T = TypeVar("T")

class TaskPool(Generic[T]):
    """
    A TaskPool is a utility that receives submitted tasks which have an identity and which should be executed no more
    than once. It can be configured to wait for the task to finish when started, wait for the task to finish when it
    is in progress, and record the result of the task when it finishes and return it when a task with the same ID is
    submitted again.
    """

    _logger = logging.getLogger(__name__)

    def __init__(self, restart_if_finished: bool = False):
        self._task_tracker: dict[object, asyncio.Event | T | None] = {}
        self._semaphore = asyncio.Semaphore()
        self._restart_task_if_finished: bool = restart_if_finished

    def take_in_precomputed_result_map(self, results: dict[object, T]) -> None:
        self._task_tracker.update(**results)

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
        # Any async item that we need to await is put into this.
        # Then we await it at the end of the function, so we can use exception-safe 'with' block without holding the semaphore too long.
        async_operation_to_wait_for = None

        async with self._semaphore:
            if self._has_task_been_submitted_yet(task_id):
                task = self._get_tracked_task(task_id)

                if not self._is_task_in_progress(task):
                    if self._restart_task_if_finished:
                        self._logger.debug(
                            "Task %s already finished but configured to restart if finished, restarting.",
                            task_id)

                        new_task = self.create_and_track_new_unstarted_task(task_id=task_id, task_function=func,
                                                                            function_args=kwargs)
                        async_operation_to_wait_for = asyncio.create_task(self._run_task_and_record_result(new_task))
                    else:
                        self._logger.debug("Task %s already finished, returning.", task_id)
                        return task
                else:
                    self._logger.debug("Task %s in progress. Waiting.", task_id)

                    async_operation_to_wait_for = asyncio.create_task(task.wait_and_get_result())
                    async_operation_to_wait_for.add_done_callback(
                        lambda _: self._logger.debug("Finished waiting for %s.", task_id))
            else:
                new_task = self.create_and_track_new_unstarted_task(task_id=task_id, task_function=func,
                                                                    function_args=kwargs)
                async_operation_to_wait_for = asyncio.create_task(self._run_task_and_record_result(new_task))

        if async_operation_to_wait_for is not None:
            return await async_operation_to_wait_for

    def _has_task_been_submitted_yet(self, task_id: object):
        return task_id in self._task_tracker.keys()

    @staticmethod
    def _is_task_in_progress(task: Any) -> bool:
        return isinstance(task, InProgressTask)

    async def _run_task_and_record_result(self, task: InProgressTask) -> T:
        task_result = await task.run_task()

        self._logger.debug("Task %s finished", task.task_id)
        await self._record_result_of_task_and_mark_finished(task=task, result=task_result)

        return task_result

    async def _record_result_of_task_and_mark_finished(self, task: InProgressTask, result: Any):
        async with self._semaphore:
            self._update_tracked_task_with_result(task.task_id, result)

        task.mark_finished()

    def create_and_track_new_unstarted_task(self, task_id: object, task_function: Any,
                                            **function_args) -> InProgressTask:
        self._logger.debug("Creating new task %s.", task_id)
        new_in_progress_task = InProgressTask(task_id=task_id, function_to_call=task_function,
                                              function_args=function_args)
        self._task_tracker[task_id] = new_in_progress_task

        return new_in_progress_task

    def _update_tracked_task_with_result(self, task_id: object, result: Any):
        self._task_tracker[task_id] = result

    def _get_tracked_task(self, task_id: object) -> InProgressTask | T | None:
        return self._task_tracker[task_id]

    def clear(self) -> None:
        self._task_tracker.clear()

    def get_results_of_all_completed_tasks(self) -> list[T]:
        def filter_func(it):
            return it is not None and not self._is_task_in_progress(it)

        return list(filter(filter_func, self._task_tracker.values()))

    def get_completed_result_or_nothing(self, task_id: object) -> T | None:
        if task_id in self._task_tracker:
            task = self._get_tracked_task(task_id)

            if self._is_task_in_progress(task):
                return None

            return task
        else:
            return None
