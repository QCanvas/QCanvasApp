import asyncio
from typing import Callable, Any

from qcanvas.QtVersionHelper.QtCore import QObject, Signal
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
        TaskPool.__init__(self, echo=True)

        self._download_progress: dict[object, Any] = {}
        self._download_progress_sem = asyncio.Semaphore()

    async def _handle_task(self, func: Callable, task_id: object, event: asyncio.Event, func_args: dict):
        sem = self._semaphore

        try:
            async for progress in func(**func_args):
                async with self._download_progress_sem:
                    self._download_progress[task_id] = progress

                self.download_progress_updated.emit(task_id, progress)
        except BaseException as e:
            # Try to maintain integrity when a task fails
            async with self._download_progress_sem:
                if task_id in self._download_progress:
                    del self._download_progress[task_id]

            async with sem:
                event.set()
                del self._results[task_id]

            self.download_failed.emit(task_id)
            raise e

        await sem.acquire()

        if self._echo: print(f"Task {task_id} finished.")

        self._results[task_id] = None
        event.set()
        sem.release()

        self.download_finished.emit(task_id)

        return None

    async def get_task_progress(self, task_id: object):
        async with self._download_progress_sem:
            if task_id in self._download_progress:
                return self._download_progress[task_id]
            else:
                return None
