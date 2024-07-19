import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Slot
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.assignments_tab.assignment_tree import AssignmentTree
from qcanvas.ui.course_viewer.tabs.resource_rich_browser import ResourceRichBrowser
from qcanvas.util.basic_fonts import bold_font
from qcanvas.util.layouts import layout, grid_layout
from qcanvas.util.ui_tools import make_truncatable

_logger = logging.getLogger(__name__)


def _bold_label(text: str) -> QLabel:
    result = QLabel(text)
    result.setFont(bold_font)
    return result


class AssignmentsTab(QWidget):
    def __init__(
        self,
        course: db.Course,
        resource_manager: ResourceManager,
        *,
        initial_sync_receipt: Optional[SyncReceipt] = None,
    ):
        super().__init__()
        self._assignment_tree = AssignmentTree(
            course, sync_receipt=initial_sync_receipt
        )
        self._placeholder_assignment_title = "No assignment selected"
        self._assignment_label = QLabel(self._placeholder_assignment_title)
        self._assignment_label.setFont(bold_font)
        self._due_date_label = QLabel("")
        self._score_label = QLabel("")
        self._info_grid = self._setup_info_grid()
        make_truncatable(self._assignment_label)
        self._viewer = ResourceRichBrowser(resource_manager)
        self.setLayout(self._setup_layout())
        self._assignment_tree.assignment_selected.connect(self._assignment_selected)
        self._assignment_tree.reexpand()

    def _setup_info_grid(self) -> QWidget:
        layout = grid_layout(
            [
                [
                    _bold_label("Due:"),
                    self._due_date_label,
                ],
                [
                    _bold_label("Score"),
                    self._score_label,
                ],
            ]
        )
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def _setup_layout(self) -> QHBoxLayout:
        h_box = QHBoxLayout()
        h_box.addWidget(self._assignment_tree, 1)
        h_box.addLayout(
            layout(QVBoxLayout, self._assignment_label, self._info_grid, self._viewer),
            2,
        )

        return h_box

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]) -> None:
        self._assignment_tree.reload(course, sync_receipt=sync_receipt)

    @Slot()
    def _assignment_selected(self, assignment: db.Assignment) -> None:
        if assignment is not None:
            _logger.debug(
                "Show assignment %s (id='%s')", assignment.name, assignment.id
            )
            self._viewer.show_content(assignment)
            self._update_info(assignment)
        else:
            self._assignment_label.setText(self._placeholder_assignment_title)
            self._show_blank()

    def _update_info(self, assignment: db.Assignment) -> None:
        _logger.debug(assignment.course.name)
        _logger.debug("Due %s", assignment.due_date)
        _logger.debug("Score %s/%s", assignment.mark, assignment.max_mark_possible)
        self._assignment_label.setText(assignment.name)

        if assignment.due_date is not None:
            self._due_date_label.setText(
                assignment.due_date.strftime("%A %Y-%m-%d %H:%M:%S")
            )
        else:
            self._due_date_label.setText("?")
        self._score_label.setText(
            f"{assignment.mark or '?'}/{assignment.max_mark_possible or '?'}"
        )

    def _show_blank(self) -> None:
        self._viewer.show_blank()
        self._info_grid.hide()
