import logging
from dataclasses import dataclass

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Slot
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import *

from qcanvas import icons
from qcanvas.ui.course_viewer.tabs.assignment_tab import AssignmentTab
from qcanvas.ui.course_viewer.tabs.mail_tab import MailTab
from qcanvas.ui.course_viewer.tabs.page_tab import PageTab
from qcanvas.util.basic_fonts import bold_font
from qcanvas.util.layouts import layout
from qcanvas.util.ui_tools import make_truncatable

_logger = logging.getLogger(__name__)


@dataclass
class _Tab:
    index: int
    icon: QIcon
    highlighted_icon: QIcon


class CourseViewer(QWidget):

    def __init__(
        self,
        course: db.Course,
        downloader: ResourceManager,
        *,
        sync_receipt: SyncReceipt,
    ):
        super().__init__()
        # todo this is a mess. there are several other messes like this too, do they all have to be a mess?
        self._course_id = course.id
        self._previous_tab_index = 0

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

        self._tab_widget = QTabWidget()
        self._tabs: dict[str, _Tab] = {}

        # self._setup_tab(
        #     name="Files",
        #     widget=self._files_tab,
        #     icon=icons.tabs.pages,
        #     highlighted_icon=icons.tabs.pages_new_content,
        # )
        self._setup_tab(
            name="Pages",
            widget=self._pages_tab,
            icon=icons.tabs.pages,
            highlighted_icon=icons.tabs.pages_new_content,
        )
        self._setup_tab(
            name="Assignments",
            widget=self._assignments_tab,
            icon=icons.tabs.assignments,
            highlighted_icon=icons.tabs.assignments_new_content,
        )
        self._setup_tab(
            name="Mail",
            widget=self._mail_tab,
            icon=icons.tabs.mail,
            highlighted_icon=icons.tabs.mail_new_content,
        )
        # self._tabs.addTab(QLabel("Not implemented"), "Panopto")  # The meme lives on!

        self.setLayout(layout(QVBoxLayout, self._course_label, self._tab_widget))

        self._tab_widget.currentChanged.connect(self._tab_changed)

        self._highlight_tabs(sync_receipt)
        # self._highlight_tab(
        #     self._tab_widget.tabText(0)
        # )  # Because the first tab always gets auto-selected

    def _setup_tab(
        self, widget: QWidget, icon: QIcon, highlighted_icon: QIcon, name: str
    ):
        index = self._tab_widget.addTab(widget, icon, name)
        self._tabs[name] = _Tab(index, icon, highlighted_icon)

    def reload(self, course: db.Course, *, sync_receipt: SyncReceipt) -> None:
        # self._files_tab.reload(course, sync_receipt=sync_receipt)
        self._pages_tab.reload(course, sync_receipt=sync_receipt)
        self._assignments_tab.reload(course, sync_receipt=sync_receipt)
        self._mail_tab.reload(course, sync_receipt=sync_receipt)
        self._highlight_tabs(sync_receipt)

    @Slot(int)
    def _tab_changed(self, index: int) -> None:
        if index != -1:
            self._unhighlight_tab(self._tab_widget.tabText(self._previous_tab_index))
            self._previous_tab_index = index

    def _highlight_tabs(self, sync_receipt: SyncReceipt) -> None:
        updates = sync_receipt.updates_by_course.get(self._course_id, None)

        if updates is not None:
            # if len(updates.updated_resources) > 0:
            #     self._highlight_tab(0)

            if len(updates.updated_pages) > 0:
                self._highlight_tab("Pages")
            else:
                self._unhighlight_tab("Pages")

            if len(updates.updated_assignments) > 0:
                self._highlight_tab("Assignments")
            else:
                self._unhighlight_tab("Assignments")

            if len(updates.updated_messages) > 0:
                self._highlight_tab("Mail")
            else:
                self._unhighlight_tab("Mail")
        else:
            for tab_name in self._tabs.keys():
                self._unhighlight_tab(tab_name)

    def _highlight_tab(self, tab_name: str) -> None:
        tab = self._tabs[tab_name]
        self._tab_widget.setTabIcon(tab.index, tab.highlighted_icon)

    def _unhighlight_tab(self, tab_name: str) -> None:
        tab = self._tabs[tab_name]
        self._tab_widget.setTabIcon(tab.index, tab.icon)
