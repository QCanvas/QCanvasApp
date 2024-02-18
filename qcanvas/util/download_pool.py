import asyncio
from typing import Callable, Any

from qcanvas.QtVersionHelper.QtCore import QObject, Signal
from qcanvas.util.task_pool import TaskPool

DOWNLOAD_FINISHED_SENTINEL = ":)"


class DownloadPool(TaskPool[None], QObject):
    """
    Like the TaskPool, but uses a queue (a channel in kotlin terms) in the task to report download progress.
    When using .submit(), it is EXPECTED that the lambda has a parameter to take in the queue, e.g:
    ```
    pool.submit(my_task_id, lambda channel: my_func(channel))

    async def my_func(channel: asyncio.Queue):
        for i in range(0, 10):
            await slow_thing()
            channel.put_nowait(i / 10) # can be whatever format/type you want

        channel.put_nowait(DOWNLOAD_FINISHED_SENTINEL)

    ```
    Where progress is put into the channel somehow.
    """
    download_progress_updated = Signal(object, Any)

    def __init__(self, parent: QObject | None = None):
        QObject.__init__(self, parent)
        TaskPool.__init__(self, echo=True)

        self._download_progress: dict[object, Any] = {}
        self._download_progress_sem = asyncio.Semaphore()

    async def _handle_task(self, func: Callable, task_id: object, event: asyncio.Event, func_args: dict):
        sem = self._semaphore

        queue = asyncio.Queue()
        # Create the task
        task = asyncio.create_task(func(queue, **func_args))

        try:
            # Take in first progress value
            progress = await asyncio.wait_for(queue.get(), 10)

            # Keep taking in progress values until we find the sentinel value
            while progress is not DOWNLOAD_FINISHED_SENTINEL:
                async with self._download_progress_sem:
                    self._download_progress[task_id] = progress

                self.download_progress_updated.emit(task_id, progress)
                # Timeout for sanity check, incase something forgets to send the sentinel
                progress = await asyncio.wait_for(queue.get(), 10)
        except BaseException as e:
            # Try to maintain integrity when a task fails

            async with self._download_progress_sem:
                if task_id in self._download_progress:
                    del self._download_progress[task_id]

            async with sem:
                event.set()
                del self._results[task_id]

            raise e

        # Wait for any weird stuff to finish
        await task

        await sem.acquire()

        if self._echo: print(f"Task {task_id} finished.")

        self._results[task_id] = None
        event.set()
        sem.release()

        return None

    def get_task_progress(self, task_id: object):
        # This can't be async because it's used from a non-async context,
        # so there is no semaphore logic here. Realistically the risk is negligible for how this function is used.

        if task_id in self._download_progress:
            return self._download_progress[task_id]
        else:
            return None
