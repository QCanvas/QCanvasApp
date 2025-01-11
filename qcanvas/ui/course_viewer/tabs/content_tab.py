import logging

from libqcanvas import db
from libqcanvas.net.resources.download.resource_manager import ResourceManager
from libqcanvas.net.sync.sync_receipt import SyncReceipt
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QWidget,
    QLayout,
)

from qcanvas.ui.course_viewer.content_tree import ContentTree
from qcanvas.ui.course_viewer.tabs.resource_rich_browser import ResourceRichBrowser

import qcanvas.util.ui_tools as ui

_logger = logging.getLogger(__name__)


class ContentTab(QWidget):
    @classmethod
    def create_from_receipt[T: ContentTab](
        cls: T,
        *,
        course: db.Course,
        sync_receipt: SyncReceipt,
        downloader: ResourceManager,
    ) -> type[T]:
        return cls(course=course, sync_receipt=sync_receipt, downloader=downloader)

    def __init__(
        self,
        *,
        explorer: ContentTree[db.Course],
        title_placeholder_text: str,
        downloader: ResourceManager,
    ):
        super().__init__()
        self.content_grid = QGridLayout()
        self._placeholder_text = title_placeholder_text
        self._title_label = self._create_title_label()
        self._use_info_grid = False
        self._info_grid = QWidget()
        self._info_grid.hide()
        self._viewer = ResourceRichBrowser(downloader=downloader)
        self._explorer = explorer

        self.setLayout(self.content_grid)
        self._setup_layout()
        self._explorer.item_selected.connect(self._item_selected)

    def enable_info_grid(self) -> None:
        self._info_grid.setLayout(self.setup_info_grid())
        self._use_info_grid = True

    def _create_title_label(self) -> QLabel:
        return ui.label(
            self._placeholder_text,
            font=ui.font(point_size=12, bold=True),
            allow_truncation=True,
        )

    def setup_info_grid(self) -> QLayout:
        """
        Override this if you need an info grid
        """
        raise NotImplementedError()

    def _setup_layout(self) -> None:
        self.content_grid.addWidget(self._explorer, 0, 0, 4, 1)
        self.content_grid.addWidget(self._title_label, 0, 1)
        self.content_grid.addWidget(self._info_grid, 1, 1)
        self.content_grid.addWidget(self._viewer, 2, 1)

    def reload(self, course: db.Course, *, sync_receipt: SyncReceipt) -> None:
        self._explorer.reload(course, sync_receipt=sync_receipt)

    @Slot(object)
    def _item_selected(self, item: object) -> None:
        if isinstance(item, db.CourseContentItem):
            _logger.debug("Show %s", item.name)
            self._show_content(item)
        else:
            self._show_blank()

    def _show_content(self, item: db.CourseContentItem) -> None:
        self._title_label.setText(item.name)
        self._viewer.show_content(item)

        if self._use_info_grid:
            self._info_grid.show()
            self.update_info_grid(item)

    def update_info_grid(self, content: db.CourseContentItem) -> None:
        raise NotImplementedError()

    def _show_blank(self) -> None:
        self._title_label.setText(self._placeholder_text)
        self._viewer.show_blank(completely_blank=True)

        if self._use_info_grid:
            self._info_grid.hide()
