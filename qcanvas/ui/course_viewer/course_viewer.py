import logging
from typing import Optional

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.assignment_tab import AssignmentTab
from qcanvas.ui.course_viewer.tabs.mail_tab import MailTab
from qcanvas.ui.course_viewer.tabs.page_tab import PageTab
from qcanvas.util.basic_fonts import bold_font
from qcanvas.util.layouts import layout
from qcanvas.util.ui_tools import make_truncatable

_logger = logging.getLogger(__name__)


class CourseViewer(QWidget):
    def __init__(
        self,
        course: db.Course,
        downloader: ResourceManager,
        *,
        initial_sync_receipt: Optional[SyncReceipt] = None
    ):
        super().__init__()
        # todo this is a mess. there are several other messes like this too, do they all have to be a mess?
        self._course_label = QLabel(course.name)
        self._course_label.setFont(bold_font)
        make_truncatable(self._course_label)
        self._pages_tab = PageTab.create_from_receipt(
            course=course,
            downloader=downloader,
            sync_receipt=initial_sync_receipt,
        )
        self._assignments_tab = AssignmentTab.create_from_receipt(
            course=course,
            downloader=downloader,
            sync_receipt=initial_sync_receipt,
        )
        self._mail_tab = MailTab.create_from_receipt(
            course=course,
            downloader=downloader,
            sync_receipt=initial_sync_receipt,
        )
        self._tabs = QTabWidget()

        self._tabs.addTab(self._pages_tab, "Pages")
        self._tabs.addTab(self._assignments_tab, "Assignments")
        self._tabs.addTab(self._mail_tab, "Mail")
        # todo: move back to first when implemented
        self._tabs.addTab(QLabel("Not implemented"), "Files")
        # self._tabs.addTab(QLabel("Not implemented"), "Panopto") The meme lives on!

        self.setLayout(layout(QVBoxLayout, self._course_label, self._tabs))

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]) -> None:
        # self._tabs.setTabText(1, "*Pages")
        self._pages_tab.reload(course, sync_receipt=sync_receipt)
        self._assignments_tab.reload(course, sync_receipt=sync_receipt)
        self._mail_tab.reload(course, sync_receipt=sync_receipt)
