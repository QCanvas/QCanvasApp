import logging
from abc import ABCMeta
from pathlib import Path

from PySide6.QtGui import QDesktopServices
from libqcanvas import db
from libqcanvas.database import QCanvasDatabase
from libqcanvas.net.resources.download.resource_manager import ResourceManager
from libqcanvas.net.resources.extracting.extractors import Extractors
from PySide6.QtCore import QObject, Signal

from qcanvas.util.qurl_util import file_url

_logger = logging.getLogger(__name__)


class _Meta(type(QObject), ABCMeta): ...


class FrontendResourceManager(QObject, ResourceManager, metaclass=_Meta):
    download_finished = Signal(db.Resource)
    download_failed = Signal(db.Resource)
    download_progress = Signal(db.Resource, int, int)

    def __init__(
        self,
        database: QCanvasDatabase,
        download_dest: Path,
        extractors: Extractors = Extractors(),
    ):
        super().__init__(
            database=database, download_dest=download_dest, extractors=extractors
        )

    async def download_and_open(self, resource: db.Resource) -> None:
        await self.download(resource)
        resource_path = file_url(self.resource_download_location(resource))
        QDesktopServices.openUrl(resource_path)

    def on_download_progress(
        self, resource: db.Resource, current: int, total: int
    ) -> None:
        self.download_progress.emit(resource, current, total)

    def on_download_failed(self, resource: db.Resource) -> None:
        self.download_failed.emit(resource)

    def on_download_finished(self, resource: db.Resource) -> None:
        self.download_finished.emit(resource)
