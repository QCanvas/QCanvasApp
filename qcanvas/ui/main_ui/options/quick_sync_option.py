import logging
from typing import *

from qtpy.QtCore import Slot
from qtpy.QtGui import QAction
from qtpy.QtWidgets import QMenu

from qcanvas.util import settings

_logger = logging.getLogger(__name__)


class QuickSyncOption(QAction):
    def __init__(self, parent: Optional[QMenu] = None):
        super().__init__("Ignore old courses", parent)
        self.setToolTip(
            "When this option is selected, old courses will not be synchronised. This will only effect the first sync."
        )
        self.setCheckable(True)
        self.setChecked(settings.client.quick_sync_enabled)
        self.triggered.connect(self._triggered)

    @Slot()
    def _triggered(self) -> None:
        settings.client.quick_sync_enabled = self.isChecked()
