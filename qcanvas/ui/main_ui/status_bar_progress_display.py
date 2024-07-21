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

    @asyncSlot()
    async def _on_task_progress(
        self, task_id: TaskID, current: int, total: int
    ) -> None:
        _logger.debug("Progress %s: %i/%i", task_id, current, total)

        async with self._lock:
            if current == total and total != 0:
                _logger.debug("Task finished %s", task_id)
                self._tasks.pop(task_id, None)
            elif task_id not in self._tasks:
                self._tasks[task_id] = _TaskProgress(current, total)
            else:
                task = self._tasks[task_id]

                task.current = current
                task.total = total

        await self._update_task_status()

    @asyncSlot()
    async def _on_task_failed(self, task_id: TaskID, context: str | Exception) -> None:
        async with self._lock:
            self._tasks.pop(task_id, None)

            if len(self._tasks) == 0:
                self._progress_bar.hide()

        self.showMessage(f"Failed: {task_id.step_name}", 5000)

    async def _update_task_status(self) -> None:
        _logger.debug("Tasks: %s", self._tasks)
        async with self._lock:
            if len(self._tasks) == 0:
                self._show_done()
            elif len(self._tasks) == 1:
                self._show_single_task_progress(list(self._tasks.items())[0])
            else:
                self._show_multiple_tasks_progress(list(self._tasks.values()))

    def _show_done(self) -> None:
        self.showMessage("All tasks finished", 5000)
        self._progress_bar.hide()

    def _show_single_task_progress(self, task: Tuple[TaskID, _TaskProgress]) -> None:
        id, progress = task

        self._show_progress(progress)
        self.showMessage(id.step_name)

    def _show_multiple_tasks_progress(self, tasks: list[_TaskProgress]) -> None:
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
