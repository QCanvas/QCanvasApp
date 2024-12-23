import logging
from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from qcanvas import icons
import qcanvas.settings as settings

_logger = logging.getLogger(__name__)


class _EnableAutoDownloadOption(QAction):
    def __init__(self, parent: Optional[QMenu] = None):
        super().__init__("Enable", parent)
        self.setCheckable(True)
        self.setChecked(settings.client.download_new_resources)
        self.triggered.connect(self._triggered)

    @Slot()
    def _triggered(self) -> None:
        settings.client.download_new_resources = self.isChecked()


class _EnableVideoDownloadOption(QAction):
    def __init__(self, parent: Optional[QMenu] = None):
        super().__init__("Include videos (slow)", parent)
        self.setCheckable(True)
        self.setChecked(settings.client.download_new_videos)
        self.triggered.connect(self._triggered)

    @Slot()
    def _triggered(self) -> None:
        settings.client.download_new_videos = self.isChecked()


class AutoDownloadResourcesMenu(QMenu):
    def __init__(self, parent: Optional[QMenu] = None):
        super().__init__("Auto download resources", parent)
        self.addAction(_EnableAutoDownloadOption(self))
        self.addAction(_EnableVideoDownloadOption(self))
        self.setIcon(icons.options.auto_download)
