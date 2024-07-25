import logging
from asyncio import Lock
from dataclasses import dataclass
from typing import *

from qasync import asyncSlot
from qcanvas_backend.task_master import TaskID
from qtpy.QtWidgets import *

from qcanvas.backend_connectors import task_master

_logger = logging.getLogger(__name__)


@dataclass
class _TaskProgress:
    current: int
    total: int


class StatusBarProgressDisplay(QStatusBar):
    def __init__(self):
        super().__init__()
        self._lock = Lock()
        self._tasks: dict[TaskID, _TaskProgress] = {}

        self._progress_bar = self._setup_progress_bar()
        self.addPermanentWidget(self._progress_bar)

        task_master.task_progress.connect(self._on_task_progress)
        task_master.task_failed.connect(self._on_task_failed)

        self.showMessage("Ready", 5000)

    def _setup_progress_bar(self) -> QProgressBar:
        bar = QProgressBar()
        bar.setTextVisible(True)
        bar.hide()
        return bar

    @asyncSlot(TaskID, int, int)
    async def _on_task_progress(
        self, task_id: TaskID, current: int, total: int
    ) -> None:
        _logger.debug("Progress %s: %i/%i", task_id, current, total)

        async with self._lock:
            if task_id not in self._tasks:
                self._add_task(task_id, current, total)
            if current == total and total != 0:
                self._remove_task(task_id)
            else:
                self._update_task(task_id, current, total)

        await self._update_task_status()

    def _update_task(self, task_id: TaskID, current: int, total: int) -> None:
        _logger.debug("Update %s", task_id)
        task = self._tasks[task_id]
        task.current = current
        task.total = total

    @asyncSlot(TaskID, object)
    async def _on_task_failed(self, task_id: TaskID, context: object) -> None:
        _logger.info("%s failed", task_id)

        async with self._lock:
            self._remove_task(task_id)

            if self._has_no_tasks:
                self._progress_bar.hide()

        self.showMessage(f"Failed: {task_id.step_name}", 5000)

    async def _update_task_status(self) -> None:
        _logger.debug("Tasks: %s", self._tasks)
        async with self._lock:
            if self._has_no_tasks:
                self._show_done()
            elif self._has_single_task:
                self._show_single_task_progress(list(self._tasks.items())[0])
            else:
                self._show_multiple_tasks_progress(list(self._tasks.values()))

    def _show_done(self) -> None:
        _logger.info("Finished tasks. Tasks: %s", self._tasks)
        self.showMessage("Done", 5000)
        self._progress_bar.hide()

    def _show_single_task_progress(self, task: Tuple[TaskID, _TaskProgress]) -> None:
        _logger.debug("Single task %s", task)
        id, progress = task

        self._show_progress(progress)
        self.showMessage(id.step_name)

    def _show_multiple_tasks_progress(self, tasks: list[_TaskProgress]) -> None:
        _logger.debug("Multiple tasks %s", tasks)
        self.showMessage(f"{len(tasks)} tasks in progress")
        self._show_progress(self._calculate_progress(tasks))

    def _calculate_progress(self, tasks: list[_TaskProgress]) -> _TaskProgress:
        # Used to represent 0..1 progress as 0..multiplier
        multiplier = 1000
        current_sum = 0
        total_sum = 0

        for task in tasks:
            if task.total != 0:
                current_sum += (task.current / task.total) * multiplier

            total_sum += multiplier

        _logger.debug(
            "%s tasks, current=%i, total=%i", len(tasks), int(current_sum), total_sum
        )

        return _TaskProgress(int(current_sum), total_sum)

    def _show_progress(self, progress: _TaskProgress) -> None:
        self._progress_bar.setMaximum(progress.total)
        self._progress_bar.setValue(progress.current)

        if progress.total != 0:
            self._progress_bar.setFormat(
                f"{(progress.current / progress.total) * 100:.0f}%"
            )
        else:
            self._progress_bar.setFormat("")

        self._progress_bar.show()

    def _add_task(self, task: TaskID, current: int, total: int) -> None:
        self._tasks[task] = _TaskProgress(current, total)
        _logger.info("Added task %s", task)
        _logger.debug("Tasks: %s", self._tasks)

    def _remove_task(self, task: TaskID) -> None:
        self._tasks.pop(task, None)
        _logger.info("Removed task %s", task)
        _logger.debug("Tasks: %s", self._tasks)

    @property
    def _has_single_task(self) -> bool:
        return len(self._tasks) == 1

    @property
    def _has_many_tasks(self) -> bool:
        return len(self._tasks) > 1

    @property
    def _has_no_tasks(self) -> bool:
        return len(self._tasks) == 0
