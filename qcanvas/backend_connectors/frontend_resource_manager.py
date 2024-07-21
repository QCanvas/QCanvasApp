import logging
from abc import ABCMeta
from pathlib import Path
from threading import Lock

import qcanvas_backend.database.types as db
from qcanvas_backend.database import QCanvasDatabase
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.resources.extracting.extractors import Extractors
from qcanvas_backend.task_master import TaskID
from qtpy.QtCore import QObject, Signal

from qcanvas.backend_connectors.qcanvas_task_master import task_master

_logger = logging.getLogger(__name__)


class _Meta(type(QObject), ABCMeta): ...


class FrontendResourceManager(QObject, ResourceManager, metaclass=_Meta):
    download_finished = Signal(db.Resource)
    download_failed = Signal(db.Resource)

    def __init__(
        self,
        database: QCanvasDatabase,
        download_dest: Path,
        extractors: Extractors = Extractors(),
    ):
        super().__init__(
            database=database, download_dest=download_dest, extractors=extractors
        )
        self._lock = Lock()
        self._download_tasks: dict[str, TaskID] = {}

    # todo will need more signals
    def on_download_progress(
        self, resource: db.Resource, current: int, total: int
    ) -> None:
        with self._lock:
            if resource.id not in self._download_tasks:
                task = TaskID("Download", resource.file_name)
                self._download_tasks[resource.id] = task
            elif current == total and total != 0:
                task = self._download_tasks.pop(resource.id, None)
            else:
                task = self._download_tasks[resource.id]

        task_master.report_progress(task, current, total)

    def on_download_failed(self, resource: db.Resource) -> None:
        with self._lock:
            task = self._download_tasks.pop(
                resource.id, TaskID("Download", resource.file_name)
            )

        task_master.report_failed(task, "Download failed")

        self.download_failed.emit(resource)

    def on_download_finished(self, resource: db.Resource) -> None:
        self.download_finished.emit(resource)
