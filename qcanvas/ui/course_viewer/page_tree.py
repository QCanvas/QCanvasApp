import logging
from typing import Optional

import qcanvas_backend.database.types as db
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import Qt

from qcanvas.ui.memory_tree import MemoryTreeWidget, MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class PageTree(MemoryTreeWidget):
    page_selected = Signal(db.ModulePage)

    def __init__(self, course: db.Course):
        super().__init__(tree_name=f"course.{course.id}.modules")
        self.selectionModel().selectionChanged.connect(self._selection_changed)
        self._last_selected_id: Optional[str] = None
        self._course = course
        self._add_items()

    def reload(self, course: db.Course):
        self._course = course
        self._add_items()

        if self._last_selected_id is not None:
            self.select_ids([self._last_selected_id])

    def _add_items(self) -> None:
        self.clear()

        widgets = []

        for module in self._course.modules:  # type: db.Module
            module_widget = MemoryTreeWidgetItem(
                id=module.id, data=module, strings=[module.name]
            )
            widgets.append(module_widget)
            module_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)

            for page in module.pages:  # type: db.ModulePage
                page_widget = MemoryTreeWidgetItem(
                    id=page.id, data=page, strings=[page.name]
                )
                page_widget.setFlags(
                    Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
                )
                module_widget.addChild(page_widget)

        self.addTopLevelItems(widgets)
        self.reexpand()

    @Slot()
    def _selection_changed(self):
        # fixme are these suppression actually needed???
        if self._suppress_selection_signal:
            return

        try:
            selected = self.selectedItems()[0]

            if not isinstance(selected, MemoryTreeWidgetItem):
                return

            if isinstance(selected.extra_data, db.ModulePage):
                self.page_selected.emit(selected.extra_data)
                self._last_selected_id = selected.extra_data.id
            else:
                self.page_selected.emit(None)
                self._last_selected_id = None
        except IndexError:
            return
