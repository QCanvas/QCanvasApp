import logging
from dataclasses import dataclass

from libqcanvas import db
from libqcanvas.net.resources.download.resource_manager import ResourceManager
from libqcanvas.net.sync.sync_receipt import SyncReceipt
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from qcanvas import icons
from qcanvas.ui.course_viewer.tabs.assignment_tab import AssignmentTab
from qcanvas.ui.course_viewer.tabs.mail_tab import MailTab
from qcanvas.ui.course_viewer.tabs.page_tab import PageTab
from qcanvas.util.layouts import layout
import qcanvas.util.ui_tools as ui

_logger = logging.getLogger(__name__)


@dataclass
class _Tab:
    icon: QIcon
    highlighted_icon: QIcon
    update_type: type


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

        self._course_label = ui.label(
            course.name, font=ui.font(point_size=13, bold=True), allow_truncation=True
        )

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
        self._tabs: dict[int, _Tab] = {}

        # self._setup_tab(
        #     name="Files",
        #     widget=self._files_tab,
        #     icon=icons.tabs.pages,
        #     highlighted_icon=icons.tabs.pages_new_content,
        # )
        self._PAGES_TAB = self._set_up_tab(
            name="Pages",
            widget=self._pages_tab,
            icon=icons.tabs.pages,
            highlighted_icon=icons.tabs.pages_new_content,
            content_update_key=db.Page,
        )
        self._ASSIGNMENTS_TAB = self._set_up_tab(
            name="Assignments",
            widget=self._assignments_tab,
            icon=icons.tabs.assignments,
            highlighted_icon=icons.tabs.assignments_new_content,
            content_update_key=db.Assignment,
        )
        self._MAIL_TAB = self._set_up_tab(
            name="Mail",
            widget=self._mail_tab,
            icon=icons.tabs.mail,
            highlighted_icon=icons.tabs.mail_new_content,
            content_update_key=db.Message,
        )
        # self._tabs.addTab(QLabel("Not implemented"), "Panopto")  # The meme lives on!

        self.setLayout(layout(QVBoxLayout, self._course_label, self._tab_widget))
        self._tab_widget.currentChanged.connect(self._tab_changed)
        self._highlight_tabs(sync_receipt)

    def _set_up_tab(
        self,
        *,
        widget: QWidget,
        icon: QIcon,
        highlighted_icon: QIcon,
        name: str,
        content_update_key: type,
    ) -> int:
        index = self._tab_widget.addTab(widget, icon, name)
        self._tabs[index] = _Tab(icon, highlighted_icon, update_type=content_update_key)
        return index

    def reload(self, course: db.Course, *, sync_receipt: SyncReceipt) -> None:
        # self._files_tab.reload(course, sync_receipt=sync_receipt)
        self._pages_tab.reload(course, sync_receipt=sync_receipt)
        self._assignments_tab.reload(course, sync_receipt=sync_receipt)
        self._mail_tab.reload(course, sync_receipt=sync_receipt)
        self._highlight_tabs(sync_receipt)

    @Slot(int)
    def _tab_changed(self, index: int) -> None:
        _logger.debug(f"Index = {index}")
        if index != -1:
            _logger.debug(f"Previous tab = {self._previous_tab_index}")
            self._set_tab_highlight(self._previous_tab_index, False)
            self._previous_tab_index = index

    def _highlight_tabs(self, sync_receipt: SyncReceipt) -> None:
        updates = sync_receipt.updates_by_course.get(self._course_id, None)

        for tab_index, tab in enumerate(self._tabs.values()):
            self._set_tab_highlight(
                tab_index, updates is not None and updates[tab.update_type] is not None
            )

    def _set_tab_highlight(self, tab_index: int, highlighted: bool) -> None:
        tab = self._tabs[tab_index]
        self._tab_widget.setTabIcon(
            tab_index, tab.highlighted_icon if highlighted else tab.icon
        )
