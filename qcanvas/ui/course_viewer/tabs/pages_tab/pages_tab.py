import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Slot
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.pages_tab.page_tree import PageTree
from qcanvas.ui.course_viewer.tabs.resource_rich_browser import ResourceRichBrowser
from qcanvas.util.basic_fonts import bold_font
from qcanvas.util.layouts import layout

_logger = logging.getLogger(__name__)


class PagesTab(QWidget):
    def __init__(
        self,
        course: db.Course,
        resource_manager: ResourceManager,
        *,
        initial_sync_receipt: Optional[SyncReceipt] = None
    ):
        super().__init__()
        self._page_tree = PageTree(course, sync_receipt=initial_sync_receipt)
        self._placeholder_page_title = "No page selected"
        self._page_label = QLabel(self._placeholder_page_title)
        self._page_label.setFont(bold_font)
        self._viewer = ResourceRichBrowser(resource_manager)

        self.setLayout(self._setup_layout())
        self._page_tree.page_selected.connect(self._page_selected)
        self._page_tree.reexpand()

    def _setup_layout(self) -> QHBoxLayout:
        h_box = QHBoxLayout()
        h_box.addWidget(self._page_tree, 1)
        h_box.addLayout(layout(QVBoxLayout, self._page_label, self._viewer), 2)

        return h_box

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]) -> None:
        self._page_tree.reload(course, sync_receipt=sync_receipt)

    @Slot()
    def _page_selected(self, page: db.ModulePage) -> None:
        if page is not None:
            _logger.debug("Show page %s (id='%s')", page.name, page.id)
            self._viewer.show_page(page)
            self._page_label.setText(page.name)
        else:
            self._page_label.setText(self._placeholder_page_label)
            self._viewer.show_blank()