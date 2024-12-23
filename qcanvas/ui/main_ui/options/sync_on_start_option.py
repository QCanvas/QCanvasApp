import logging
from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

import qcanvas.settings as settings

_logger = logging.getLogger(__name__)


class SyncOnStartOption(QAction):
    def __init__(self, parent: Optional[QMenu] = None):
        super().__init__("Sync on start", parent)
        self.setToolTip(
            "When enabled, synchronisation will start when the application is opened."
        )
        self.setCheckable(True)
        self.setChecked(settings.client.sync_on_start)
        self.triggered.connect(self._triggered)
        # self.set(icons.options.sync_on_start)

    @Slot()
    def _triggered(self) -> None:
        settings.client.sync_on_start = self.isChecked()
