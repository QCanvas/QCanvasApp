import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.assignment_tab.assignment_tree import AssignmentTree
from qcanvas.ui.course_viewer.tabs.content_tab import ContentTab
from qcanvas.ui.course_viewer.tabs.util import date_strftime_format
from qcanvas.util.basic_fonts import bold_label
from qcanvas.util.layouts import grid_layout

_logger = logging.getLogger(__name__)


class AssignmentTab(ContentTab):
    @staticmethod
    def create_from_receipt(
        *,
        course: db.Course,
        sync_receipt: Optional[SyncReceipt],
        downloader: ResourceManager,
    ) -> "AssignmentTab":
        return AssignmentTab(
            course=course, sync_receipt=sync_receipt, downloader=downloader
        )

    def __init__(
        self,
        *,
        course: db.Course,
        sync_receipt: Optional[SyncReceipt],
        downloader: ResourceManager,
    ):
        super().__init__(
            explorer=AssignmentTree.create_from_receipt(
                course, sync_receipt=sync_receipt
            ),
            title_placeholder_text="No assignment selected",
            downloader=downloader,
        )

        self._due_date_label = QLabel("")
        self._score_label = QLabel("")

        self.enable_info_grid()

    def setup_info_grid(self) -> QGridLayout:
        grid = grid_layout(
            [
                [
                    bold_label("Due:"),
                    self._due_date_label,
                ],
                [
                    bold_label("Score:"),
                    self._score_label,
                ],
            ]
        )

        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)

        return grid

    def update_info_grid(self, assignment: db.Assignment) -> None:
        if assignment.due_date is not None:
            due_text = assignment.due_date.strftime(date_strftime_format)
        else:
            due_text = "?"

        self._due_date_label.setText(due_text)

        self._score_label.setText(
            f"{assignment.mark or '?'}/{assignment.max_mark_possible or '?'}"
        )

    # def __init__(
    #     self,
    #     course: db.Course,
    #     resource_manager: ResourceManager,
    #     *,
    #     initial_sync_receipt: Optional[SyncReceipt] = None,
    # ):
    #     super().__init__()
    #     self._assignment_tree = AssignmentTree(
    #         course, sync_receipt=initial_sync_receipt
    #     )
    #     self._placeholder_assignment_title = "No assignment selected"
    #     self._assignment_label = QLabel(self._placeholder_assignment_title)
    #     self._assignment_label.setFont(bold_font)
    #     self._due_date_label = QLabel("")
    #     self._score_label = QLabel("")
    #     self._info_grid = self._setup_info_grid()
    #     make_truncatable(self._assignment_label)
    #     self._viewer = ResourceRichBrowser(resource_manager)
    #     self.setLayout(self._setup_layout())
    #     self._assignment_tree.assignment_selected.connect(self._assignment_selected)
    #     self._assignment_tree.reexpand()
    #
    # def _setup_info_grid(self) -> QWidget:
    #     layout = grid_layout(
    #         [
    #             [
    #                 _bold_label("Due:"),
    #                 self._due_date_label,
    #             ],
    #             [
    #                 _bold_label("Score:"),
    #                 self._score_label,
    #             ],
    #         ]
    #     )
    #     layout.setColumnStretch(0, 0)
    #     layout.setColumnStretch(1, 1)
    #
    #     widget = QWidget()
    #     widget.setLayout(layout)
    #
    #     return widget
    #
    # def _setup_layout(self) -> QHBoxLayout:
    #     h_box = QHBoxLayout()
    #     h_box.addWidget(self._assignment_tree, 1)
    #     h_box.addLayout(
    #         layout(QVBoxLayout, self._assignment_label, self._info_grid, self._viewer),
    #         2,
    #     )
    #
    #     return h_box
    #
    # def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]) -> None:
    #     self._assignment_tree.reload(course, sync_receipt=sync_receipt)
    #
    # @Slot()
    # def _assignment_selected(self, assignment: db.Assignment) -> None:
    #     if assignment is not None:
    #         _logger.debug(
    #             "Show assignment %s (id='%s')", assignment.name, assignment.id
    #         )
    #         self._viewer.show_content(assignment)
    #         self._update_info(assignment)
    #     else:
    #         self._assignment_label.setText(self._placeholder_assignment_title)
    #         self._show_blank()
    #
    # def _update_info(self, assignment: db.Assignment) -> None:
    #     _logger.debug(assignment.course.name)
    #     _logger.debug("Due %s", assignment.due_date)
    #     _logger.debug("Score %s/%s", assignment.mark, assignment.max_mark_possible)
    #     self._assignment_label.setText(assignment.name)
    #
    #     if assignment.due_date is not None:
    #         self._due_date_label.setText(
    #             assignment.due_date.strftime("%A %Y-%m-%d %H:%M:%S")
    #         )
    #     else:
    #         self._due_date_label.setText("?")
    #     self._score_label.setText(
    #         f"{assignment.mark or '?'}/{assignment.max_mark_possible or '?'}"
    #     )
    #
    # def _show_blank(self) -> None:
    #     self._viewer.show_blank()
    #     self._info_grid.hide()
