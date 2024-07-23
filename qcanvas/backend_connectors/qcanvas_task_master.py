import logging
from abc import ABCMeta

from qcanvas_backend.task_master import TaskID, TaskMaster, set_global_task_master
from qtpy.QtCore import QObject, Signal

_logger = logging.getLogger(__name__)


class _Meta(type(QObject), ABCMeta): ...


class _TaskMaster(TaskMaster, QObject, metaclass=_Meta):
    task_progress = Signal(TaskID, int, int)
    task_failed = Signal(TaskID, object)

    def report_failed(self, _task_id: TaskID, context: object) -> None:
        self.task_failed.emit(_task_id, context)

    def report_progress(self, _task_id: TaskID, current: int, total: int) -> None:
        self.task_progress.emit(_task_id, current, total)


task_master = _TaskMaster()


def register():
    set_global_task_master(task_master)
