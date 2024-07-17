import logging

import qcanvas_backend.database.types as db
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import Qt

from qcanvas.ui.memory_tree import MemoryTreeWidget, MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class AssignmentTree(MemoryTreeWidget):
    page_selected = Signal(db.ModulePage)

    def __init__(self, course: db.Course):
        super().__init__(tree_name=f"course.{course.id}.assignments")
        self.selectionModel().selectionChanged.connect(self._selection_changed)
        self._course = course
        self._add_items()

    def _add_items(self) -> None:
        self.clear()

        widgets = []

        for module in self._course.assignment_groups:  # type: db.AssignmentGroup
            module_widget = MemoryTreeWidgetItem(
                id=module.id, data=module, strings=[module.name]
            )
            widgets.append(module_widget)
            module_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)

            for page in module.assignments:  # type: db.Assignment
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
        try:
            selected: MemoryTreeWidgetItem = self.selectedItems()[0]

            if isinstance(selected.extra_data, db.Assignment):
                _logger.debug(selected.extra_data.max_mark_possible)
                self.page_selected.emit(selected.extra_data)
            else:
                self.page_selected.emit(None)
        except IndexError:
            return
