from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget
from qasync import asyncSlot

from qcanvas.backend_connectors import FrontendResourceManager
from .qml_bridge_types import Attachment
from .qml_pane import QmlPane
from libqcanvas import db
import logging

_logger = logging.getLogger(__name__)


class AttachmentsPane(QmlPane):
    def __init__(
        self, downloader: FrontendResourceManager, parent: QWidget | None = None
    ):
        super().__init__(Path(__file__).parent / "AttachmentsPane.qml", parent)

        self._original_dock_name = None
        self._downloader = downloader
        self._files: dict[str, db.Resource] = {}
        self._qfiles: dict[str, Attachment] = {}
        self.ctx["submission_files"] = []
        self.load_view()

        self._downloader.download_finished.connect(self._download_updated)
        self._downloader.download_failed.connect(self._download_updated)

    def clear_files(self):
        self.ctx["submission_files"] = []
        self._files.clear()
        self._qfiles.clear()

    def load_files(self, files: list[db.Resource]):
        qfiles = []

        if self._original_dock_name is None:
            self._original_dock_name = self.parent().windowTitle()

        self.parent().setWindowTitle(f"{self._original_dock_name} ({len(files)})")

        for file in files:
            qfile = Attachment(
                file_name=file.file_name,
                resource_id=file.id,
                download_state=file.download_state,
            )
            qfile.opened.connect(self._on_attachment_opened)
            qfiles.append(qfile)

            self._qfiles[file.id] = qfile
            self._files[file.id] = file

        self.ctx["submission_files"] = qfiles

    @asyncSlot(str)
    async def _on_attachment_opened(self, resource_id: str) -> None:
        if resource_id in self._files:
            await self._downloader.download_and_open(self._files[resource_id])
        else:
            _logger.warning(
                "User opened an attachment that doesn't belong to any comment! id=%s",
                resource_id,
            )

    @Slot(db.Resource)
    def _download_updated(self, resource: db.Resource) -> None:
        if resource.id in self._files:
            self._qfiles[resource.id].download_state = resource.download_state
