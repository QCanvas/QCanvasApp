import logging
from typing import Sequence

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QHeaderView

from qcanvas.ui.course_viewer.content_tree import ContentTree
from qcanvas.ui.memory_tree import MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class AssignmentTree(ContentTree[db.Course]):
    def __init__(self, course_id: str):
        super().__init__(
            tree_name=f"course.{course_id}.assignment_groups",
            emit_selection_signal_for_type=db.Assignment,
        )
        self.ui_setup(
            header_text=["Assignments", "Weight"],
            indentation=15,
            max_width=350,
            min_width=150,
        )

        self._adjust_header()

    def _adjust_header(self) -> None:
        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(False)

    def create_tree_items(
        self, course: db.Course, sync_receipt: SyncReceipt
    ) -> Sequence[MemoryTreeWidgetItem]:
        widgets = []

        for assignment_group in course.assignment_groups:  # type: db.AssignmentGroup
            assignment_group_widget = self._create_assignment_group_widget(
                assignment_group, sync_receipt
            )

            widgets.append(assignment_group_widget)
            for assignment in assignment_group.assignments:  # type: db.Assignment
                assignment_widget = self._create_assignment_widget(
                    assignment, sync_receipt
                )

                assignment_group_widget.addChild(assignment_widget)

        return widgets

    def _create_assignment_group_widget(
        self, assignment_group: db.AssignmentGroup, sync_receipt: SyncReceipt
    ) -> MemoryTreeWidgetItem:
        assignment_group_widget = MemoryTreeWidgetItem(
            id=assignment_group.id,
            data=assignment_group,
            strings=[assignment_group.name, f"{assignment_group.group_weight}%"],
        )

        assignment_group_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)

        if sync_receipt.was_updated(assignment_group):
            self.mark_as_unseen(assignment_group_widget)

        return assignment_group_widget

    def _create_assignment_widget(
        self, assignment: db.Assignment, sync_receipt: SyncReceipt
    ) -> MemoryTreeWidgetItem:
        assignment_widget = MemoryTreeWidgetItem(
            id=assignment.id, data=assignment, strings=[assignment.name]
        )

        assignment_widget.setFlags(
            Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        )

        if sync_receipt.was_updated(assignment):
            self.mark_as_unseen(assignment_widget)

        return assignment_widget
