import logging
from typing import Optional

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import Qt
from qtpy.QtWidgets import QHeaderView

from qcanvas.ui.memory_tree import MemoryTreeWidget, MemoryTreeWidgetItem
from qcanvas.util.basic_fonts import bold_font, normal_font

_logger = logging.getLogger(__name__)


class AssignmentTree(MemoryTreeWidget):
    assignment_selected = Signal(db.Assignment)

    def __init__(
        self, course: db.Course, *, sync_receipt: Optional[SyncReceipt] = None
    ):
        super().__init__(tree_name=f"course.{course.id}.assignments")

        self._last_selected_id: Optional[str] = None
        self._course = course

        self.selectionModel().selectionChanged.connect(self._selection_changed)
        self.setHeaderLabels(["Assignments", "Weight"])
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setStretchLastSection(False)
        self.setIndentation(15)
        self.setMaximumWidth(350)
        self.setMinimumWidth(150)

        self._add_items(sync_receipt)

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]) -> None:
        self._course = course
        self._add_items(sync_receipt)

        if self._last_selected_id is not None:
            if not self.select_ids([self._last_selected_id]):
                self._last_selected_id = None
                self.assignment_selected.emit(None)

    def _add_items(self, sync_receipt: Optional[SyncReceipt] = None) -> None:
        self.clear()

        widgets = []

        for (
            assignment_group
        ) in self._course.assignment_groups:  # type: db.AssignmentGroup
            assignment_group_widget = MemoryTreeWidgetItem(
                id=assignment_group.id,
                data=assignment_group,
                strings=[assignment_group.name, f"{assignment_group.group_weight}%"],
            )
            assignment_group_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)

            is_new = (
                sync_receipt is not None
                and assignment_group.id in sync_receipt.updated_assignment_groups
            )
            if is_new:
                assignment_group_widget.setFont(0, bold_font)

            widgets.append(assignment_group_widget)

            for assignment in assignment_group.assignments:  # type: db.Assignment
                assignment_widget = MemoryTreeWidgetItem(
                    id=assignment.id, data=assignment, strings=[assignment.name]
                )
                assignment_widget.setFlags(
                    Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
                )

                is_new = (
                    sync_receipt is not None
                    and assignment.id in sync_receipt.updated_assignments
                )
                if is_new:
                    assignment_widget.setFont(0, bold_font)

                assignment_group_widget.addChild(assignment_widget)

        self.addTopLevelItems(widgets)
        self.reexpand()

    @Slot()
    def _selection_changed(self) -> None:
        try:
            selected = self.selectedItems()[0]
        except IndexError:
            return

        if not isinstance(selected, MemoryTreeWidgetItem):
            return

        if selected.font(0).bold():
            selected.setFont(0, normal_font)

        if isinstance(selected.extra_data, db.Assignment):
            self.assignment_selected.emit(selected.extra_data)
            self._last_selected_id = selected.extra_data.id
        else:
            self.assignment_selected.emit(None)
            self._last_selected_id = None
