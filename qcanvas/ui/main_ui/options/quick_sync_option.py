import logging
from typing import *

from qtpy.QtCore import Slot
from qtpy.QtGui import QAction
from qtpy.QtWidgets import QMenu

from qcanvas import icons
from qcanvas.util import settings

_logger = logging.getLogger(__name__)


class QuickSyncOption(QAction):
    def __init__(self, parent: Optional[QMenu] = None):
        super().__init__("Ignore old courses", parent)
        self.setToolTip(
            "When enabled, old courses will not be synchronised. This won't hide any old courses that were previously synchronised."
        )
        self.setCheckable(True)
        self.setChecked(settings.client.quick_sync_enabled)
        self.triggered.connect(self._triggered)
        # self.setIcon(icons.options.ignore_old)

    @Slot()
    def _triggered(self) -> None:
        settings.client.quick_sync_enabled = self.isChecked()
