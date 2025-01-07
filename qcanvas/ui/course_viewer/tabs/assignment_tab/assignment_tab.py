import logging

from libqcanvas import db
from libqcanvas.net.resources.download.resource_manager import ResourceManager
from libqcanvas.net.sync.sync_receipt import SyncReceipt
from libqcanvas.util import as_local
from PySide6.QtWidgets import (
    QLabel,
    QLayout,
)
from typing_extensions import override

import qcanvas.util.ui_tools as ui
from .assignment_tree import AssignmentTree
from .comments_pane import CommentsPane
from qcanvas.ui.course_viewer.tabs.content_tab import ContentTab
from qcanvas.ui.course_viewer.tabs.util import (
    date_strftime_format,
)

_logger = logging.getLogger(__name__)


class AssignmentTab(ContentTab):
    def __init__(
        self,
        *,
        course: db.Course,
        sync_receipt: SyncReceipt,
        downloader: ResourceManager,
    ):
        self.comments_pane = CommentsPane()

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

    @override
    def _setup_layout(self) -> None:
        super()._setup_layout()

        self.comments_pane.hide()
        self.content_grid.addWidget(self.comments_pane, 2, 2, 1, 1)
        self.content_grid.setColumnStretch(0, 1)
        self.content_grid.setColumnStretch(1, 2)

    @override
    def setup_info_grid(self) -> QLayout:
        return ui.form_layout(
            {"Due": self._due_date_label, "Score": self._score_label},
        )

    @override
    def update_info_grid(self, assignment: db.Assignment) -> None:
        if assignment.due_date is not None:
            due_text = as_local(assignment.due_date).strftime(date_strftime_format)
        else:
            due_text = "No due date"

        self._due_date_label.setText(due_text)

        last_submission = assignment.submissions[-1] if assignment.submissions else None
        submission_score = "-"

        if last_submission and last_submission.score:
            submission_score = last_submission.score

        self._score_label.setText(f"{submission_score}/{assignment.max_score or '?'}")

        self.comments_pane.clear_comments()

        if last_submission and last_submission.comments:
            self.comments_pane.load_comments(last_submission.comments)
            self._show_comments()
        else:
            self._hide_comments()

    def _show_comments(self):
        self.comments_pane.show()
        self.content_grid.setColumnStretch(2, 2)

    def _hide_comments(self):
        self.comments_pane.hide()
        self.content_grid.setColumnStretch(2, 0)
