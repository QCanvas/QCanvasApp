import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.content_tree import ContentTree
from qcanvas.ui.course_viewer.tabs.resource_rich_browser import ResourceRichBrowser
from qcanvas.util.basic_fonts import bold_font
from qcanvas.util.ui_tools import make_truncatable

_logger = logging.getLogger(__name__)


class ContentTab(QWidget):
    def __init__(
        self,
        *,
        explorer: ContentTree,
        title_placeholder_text: str,
        downloader: ResourceManager,
    ):
        super().__init__()
        self._content_vbox = QVBoxLayout()
        self._placeholder_text = title_placeholder_text
        self._title_label = self._create_title_label()
        self._info_grid: Optional[QWidget] = None
        self._viewer = ResourceRichBrowser(resource_manager=downloader)
        self._explorer = explorer

        self._setup_layout()
        self._explorer.item_selected.connect(self._item_selected)

    def enable_info_grid(self) -> None:
        # Info grid needs to be a widget, so it can be hidden/shown
        grid_layout = self.setup_info_grid()

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        grid_widget.hide()

        self._info_grid = grid_widget
        self._content_vbox.insertWidget(1, grid_widget)

    def _create_title_label(self) -> QLabel:
        title_label = QLabel(self._placeholder_text)
        title_label.setFont(bold_font)
        make_truncatable(title_label)
        return title_label

    def setup_info_grid(self) -> QGridLayout:
        """
        Override this if you need an info grid
        """
        raise NotImplementedError()

    def _setup_layout(self) -> None:
        parent_layout = QHBoxLayout()
        parent_layout.addWidget(self._explorer)

        self._content_vbox.addWidget(self._title_label)
        self._content_vbox.addWidget(self._viewer)

        parent_layout.addLayout(self._content_vbox)

        self.setLayout(parent_layout)

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]) -> None:
        self._explorer.reload(course, sync_receipt=sync_receipt)

    def _item_selected(self, item: object) -> None:
        if isinstance(item, db.CourseContentItem):
            _logger.debug("Show %s", item.name)
            self._show_content(item)
        else:
            self._show_blank()

    def _show_content(self, item: db.CourseContentItem) -> None:
        self._title_label.setText(item.name)
        self._viewer.show_content(item)

        if self._info_grid is not None:
            self._info_grid.show()
            self.update_info_grid(item)

    def update_info_grid(self, content: db.CourseContentItem) -> None:
        raise NotImplementedError()

    def _show_blank(self) -> None:
        self._title_label.setText(self._placeholder_text)
        self._viewer.show_blank(completely_blank=True)

        if self._info_grid is not None:
            self._info_grid.hide()
