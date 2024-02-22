import asyncio
from typing import Callable, Any

from PySide6.QtCore import QObject, Signal

from qcanvas.util.task_pool import TaskPool


class DownloadPool(TaskPool[None], QObject):
    """
    Like the TaskPool, but uses a queue (a channel in kotlin terms) in the task to report download progress.
    When using .submit(), it is EXPECTED that the lambda returns a function that uses yield to signal progress, e.g:
    ```
    pool.submit(my_task_id, lambda: my_func())

    async def my_func(channel: asyncio.Queue):
        for i in range(0, 10):
            await slow_thing()
            yield (i / 10) # can be whatever format/type you want
    ```
    """
    download_progress_updated = Signal(object, Any)
    download_failed = Signal(object)
    download_finished = Signal(object)

    def __init__(self, parent: QObject | None = None):
        QObject.__init__(self, parent)
        TaskPool.__init__(self)

    async def _handle_task(self, func: Callable, task_id: object, event: asyncio.Event, func_args: dict):
        sem = self._semaphore

        try:
            # Consume progress updates 'yield'ed from the function
            async for progress in func(**func_args):
                # Fire the download progress update signal
                self.download_progress_updated.emit(task_id, progress)
        except BaseException as e:
            # Try to maintain integrity when a task fails
            async with sem:
                # Release anything else waiting for this task
                event.set()
                # Remove the record from the results map
                del self._results[task_id]

            # Emit failure signal and rethrow
            self.download_failed.emit(task_id)
            raise e

        async with sem:
            self._logger.debug("Task %s finished.", task_id)
            # Record this task as done
            self._results[task_id] = None
            event.set()

        self.download_finished.emit(task_id)

        return None