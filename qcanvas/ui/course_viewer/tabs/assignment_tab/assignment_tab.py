import logging

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

    def __init__(
        self,
        *,
        course: db.Course,
        sync_receipt: SyncReceipt,
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
