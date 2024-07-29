import logging

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Slot
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
        sync_receipt: SyncReceipt
    ):
        super().__init__()
        # todo this is a mess. there are several other messes like this too, do they all have to be a mess?
        self._course_id = course.id

        self._course_label = QLabel(course.name)
        self._course_label.setFont(bold_font)
        make_truncatable(self._course_label)

        self._pages_tab = PageTab.create_from_receipt(
            course=course,
            downloader=downloader,
            sync_receipt=sync_receipt,
        )
        self._assignments_tab = AssignmentTab.create_from_receipt(
            course=course,
            downloader=downloader,
            sync_receipt=sync_receipt,
        )
        self._mail_tab = MailTab.create_from_receipt(
            course=course,
            downloader=downloader,
            sync_receipt=sync_receipt,
        )
        # self._files_tab = FileTab.create_from_receipt(
        #     course=course,
        #     downloader=downloader,
        #     sync_receipt=sync_receipt,
        # )

        self._tabs = QTabWidget()
        self._tabs.addTab(self._pages_tab, "Pages")
        self._tabs.addTab(self._assignments_tab, "Assignments")
        self._tabs.addTab(self._mail_tab, "Mail")
        self._tabs.addTab(QLabel("Not implemented"), "Files")
        # self._tabs.addTab(self._files_tab, "Files")
        # self._tabs.addTab(QLabel("Not implemented"), "Panopto")  # The meme lives on!

        self.setLayout(layout(QVBoxLayout, self._course_label, self._tabs))

        self._tabs.currentChanged.connect(self._tab_changed)

        self._highlight_tabs(sync_receipt)
        self._unhighlight_tab(0)  # Because the first tab always gets auto-selected

    def reload(self, course: db.Course, *, sync_receipt: SyncReceipt) -> None:
        self._pages_tab.reload(course, sync_receipt=sync_receipt)
        self._assignments_tab.reload(course, sync_receipt=sync_receipt)
        self._mail_tab.reload(course, sync_receipt=sync_receipt)

        self._highlight_tabs(sync_receipt)

    @Slot(int)
    def _tab_changed(self, index: int) -> None:
        if index != -1:
            self._unhighlight_tab(index)

    def _highlight_tabs(self, sync_receipt: SyncReceipt) -> None:
        updates = sync_receipt.updates_by_course.get(self._course_id, None)

        if updates is not None:
            # if len(updates.updated_resources) > 0:
            #     raise Exception("Looks like you forgot to update the other numbers??????"")
            #     self._highlight_tab(0)

            if len(updates.updated_pages) > 0:
                self._highlight_tab(0)

            if len(updates.updated_assignments) > 0:
                self._highlight_tab(1)

            if len(updates.updated_messages) > 0:
                self._highlight_tab(2)
        else:
            for index in range(0, 4):
                self._unhighlight_tab(index)

    def _highlight_tab(self, tab_index: int) -> None:
        self._tabs.setTabText(tab_index, "* " + self._tabs.tabText(tab_index))

    def _unhighlight_tab(self, tab_index: int) -> None:
        self._tabs.setTabText(
            tab_index, self._tabs.tabText(tab_index).replace("* ", "")
        )
