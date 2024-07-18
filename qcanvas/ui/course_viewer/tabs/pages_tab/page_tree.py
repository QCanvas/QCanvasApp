import logging
from typing import Optional

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import Qt

from qcanvas.ui.memory_tree import MemoryTreeWidget, MemoryTreeWidgetItem
from qcanvas.util.basic_fonts import bold_font, normal_font

_logger = logging.getLogger(__name__)


class PageTree(MemoryTreeWidget):
    page_selected = Signal(db.ModulePage)

    def __init__(self, course: db.Course):
        super().__init__(tree_name=f"course.{course.id}.modules")

        self._last_selected_id: Optional[str] = None
        self._course = course

        self.setHeaderLabel("Content")
        self.setIndentation(15)
        self.selectionModel().selectionChanged.connect(self._selection_changed)
        self._add_items()

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]):
        self._course = course
        self._add_items(sync_receipt)

        if self._last_selected_id is not None:
            if not self.select_ids([self._last_selected_id]):
                self._last_selected_id = None
                self.page_selected.emit(None)

    def _add_items(self, sync_receipt: Optional[SyncReceipt] = None) -> None:
        self.clear()

        widgets = []

        for module in self._course.modules:  # type: db.Module
            module_widget = MemoryTreeWidgetItem(
                id=module.id, data=module, strings=[module.name]
            )
            module_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)

            is_new = (
                sync_receipt is not None and module.id in sync_receipt.updated_modules
            )
            if is_new:
                module_widget.setFont(0, bold_font)

            widgets.append(module_widget)

            for page in module.pages:  # type: db.ModulePage
                page_widget = MemoryTreeWidgetItem(
                    id=page.id, data=page, strings=[page.name]
                )
                page_widget.setFlags(
                    Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
                )

                is_new = (
                    sync_receipt is not None and page.id in sync_receipt.updated_pages
                )
                if is_new:
                    page_widget.setFont(0, bold_font)

                module_widget.addChild(page_widget)

        self.addTopLevelItems(widgets)
        self.reexpand()

    @Slot()
    def _selection_changed(self):
        try:
            selected = self.selectedItems()[0]
        except IndexError:
            return

        if not isinstance(selected, MemoryTreeWidgetItem):
            return

        if selected.font(0).bold():
            selected.setFont(0, normal_font)

        if isinstance(selected.extra_data, db.ModulePage):
            self.page_selected.emit(selected.extra_data)
            self._last_selected_id = selected.extra_data.id
        else:
            self.page_selected.emit(None)
            self._last_selected_id = None
