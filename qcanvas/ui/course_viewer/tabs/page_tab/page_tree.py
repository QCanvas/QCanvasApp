import logging
from typing import Sequence

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Qt

from qcanvas import icons
from qcanvas.ui.course_viewer.content_tree import ContentTree
from qcanvas.ui.course_viewer.tree_widget_data_item import TreeWidgetDataItem
from qcanvas.ui.memory_tree import MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class PageTree(ContentTree[db.Course]):
    def __init__(self, course_id: str):
        super().__init__(
            tree_name=f"course.{course_id}.modules",
            emit_selection_signal_for_type=db.ModulePage,
        )

        self.ui_setup(
            header_text="Content", indentation=15, max_width=300, min_width=150
        )

    def create_tree_items(
        self, course: db.Course, sync_receipt: SyncReceipt
    ) -> Sequence[MemoryTreeWidgetItem]:
        widgets = []

        for module in course.modules:  # type: db.Module
            if len(module.pages) == 0:
                continue

            module_widget = self._create_module_widget(module)
            widgets.append(module_widget)

            for page in module.pages:  # type: db.ModulePage
                page_widget = self._create_page_widget(page, sync_receipt)
                module_widget.addChild(page_widget)

        return widgets

    def _create_module_widget(self, module: db.Module) -> MemoryTreeWidgetItem:
        module_widget = MemoryTreeWidgetItem(
            id=module.id, data=module, strings=[module.name]
        )
        module_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)
        module_widget.setIcon(0, icons.tree_items.module)

        return module_widget

    def _create_page_widget(
        self, page: db.ModulePage, sync_receipt: SyncReceipt
    ) -> TreeWidgetDataItem:
        page_widget = TreeWidgetDataItem(id=page.id, data=page, strings=[page.name])
        page_widget.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        page_widget.setIcon(0, icons.tree_items.page)

        if sync_receipt.was_updated(page):
            self.mark_as_unseen(page_widget)

        return page_widget
