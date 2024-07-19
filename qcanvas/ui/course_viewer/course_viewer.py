import logging
from typing import Optional

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.pages_tab import PagesTab
from qcanvas.util.basic_fonts import bold_font
from qcanvas.util.layouts import layout

_logger = logging.getLogger(__name__)


class CourseViewer(QWidget):
    def __init__(
        self,
        course: db.Course,
        page_resource_manager: ResourceManager,
        *,
        initial_sync_receipt: Optional[SyncReceipt] = None
    ):
        super().__init__()

        self._course_label = QLabel(course.name)
        self._course_label.setFont(bold_font)
        self._course_label.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed
        )
        self._pages_tab = PagesTab(
            course, page_resource_manager, initial_sync_receipt=initial_sync_receipt
        )
        self._tabs = QTabWidget()

        self._tabs.addTab(QLabel("Not implemented"), "Files")
        self._tabs.addTab(self._pages_tab, "Pages")
        self._tabs.addTab(QLabel("Not implemented"), "Assignments")
        self._tabs.addTab(QLabel("Not implemented"), "Mail")
        # self._tabs.addTab(QLabel("Not implemented"), "Panopto") The meme lives on!

        self.setLayout(layout(QVBoxLayout, self._course_label, self._tabs))

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]) -> None:
        # self._tabs.setTabText(1, "*Pages")
        self._pages_tab.reload(course, sync_receipt=sync_receipt)
