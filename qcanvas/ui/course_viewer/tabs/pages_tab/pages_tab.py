import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Slot
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.pages_tab.page_tree import PageTree
from qcanvas.ui.course_viewer.tabs.resource_rich_browser import ResourceRichBrowser

_logger = logging.getLogger(__name__)


class PagesTab(QWidget):
    def __init__(self, course: db.Course, resource_manager: ResourceManager):
        super().__init__()
        self._page_tree = PageTree(course)
        self._viewer = ResourceRichBrowser(resource_manager)

        self.setLayout(self._setup_layout())
        self._page_tree.page_selected.connect(self._page_selected)
        self._page_tree.reexpand()

    def _setup_layout(self) -> QHBoxLayout:
        h_box = QHBoxLayout()
        h_box.addWidget(self._page_tree, 1)
        h_box.addWidget(self._viewer, 4)

        return h_box

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]):
        self._page_tree.reload(course, sync_receipt=sync_receipt)

    @Slot()
    def _page_selected(self, page: db.ModulePage):
        if page is not None:
            _logger.debug("Show page %s (id='%s')", page.name, page.id)
            self._viewer.show_page(page)
