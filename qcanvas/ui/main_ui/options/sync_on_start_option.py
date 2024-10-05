import logging
from typing import *

from qtpy.QtCore import Slot
from qtpy.QtGui import QAction
from qtpy.QtWidgets import QMenu

from qcanvas import icons
from qcanvas.util import settings

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
