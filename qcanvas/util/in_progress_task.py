import asyncio
from typing import Any


class InProgressTask:
    class _NoResult:
        pass

    def __init__(self, task_id: object, function_to_call: Any, **function_args):
        self._event = asyncio.Event()
        self._task_id = task_id
        self._function_to_call = function_to_call
        self._function_args = function_args
        self._task_result = InProgressTask._NoResult()

    async def wait_and_get_result(self) -> Any:
        await self._event.wait()
        return self._task_result

    async def run_task(self) -> Any:
        self._task_result = await self._function_to_call(**self._function_args)
        return self._task_result

    def mark_finished(self):
        self._event.set()

    @property
    def task_id(self):
        return self._task_id

    @property
    def task_result(self):
        if isinstance(self._task_result, InProgressTask._NoResult):
            raise RuntimeError("Task does not have a result yet")
        else:
            return self._task_result
