import logging

from PySide6.QtCore import Qt
from libqcanvas import db
from libqcanvas.net.sync.sync_receipt import SyncReceipt
from libqcanvas.util import as_local
from PySide6.QtWidgets import (
    QLabel,
    QLayout,
    QDockWidget,
    QMainWindow,
)
from typing_extensions import override

import qcanvas.util.ui_tools as ui
from qcanvas.backend_connectors import FrontendResourceManager
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
        downloader: FrontendResourceManager,
    ):
        # must be before super init, otherwise _setup_layout will be called before it is initialised
        self._main_container = QMainWindow()

        super().__init__(
            explorer=AssignmentTree.create_from_receipt(
                course, sync_receipt=sync_receipt
            ),
            title_placeholder_text="No assignment selected",
            downloader=downloader,
        )

        self._comments_pane = CommentsPane(downloader)
        self._comments_dock = ui.dock_widget(
            title="Comments",
            name="comments_dock",
            widget=self._comments_pane,
            min_size=ui.size(150, 150),
            features=QDockWidget.DockWidgetFeature.DockWidgetMovable,
        )
        self._main_container.setCentralWidget(self._viewer)
        self._main_container.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea, self._comments_dock
        )

        self._due_date_label = QLabel("")
        self._score_label = QLabel("")
        self.enable_info_grid()

    @override
    def _setup_layout(self) -> None:
        super()._setup_layout()
        self.content_grid.replaceWidget(self._viewer, self._main_container)

    @override
    def setup_info_grid(self) -> QLayout:
        return ui.form_layout(
            {"Due": self._due_date_label, "Score": self._score_label},
        )

    # fixme: kind of a misleading name? it's not just updating the info "grid" anymore
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

        self._comments_pane.clear_comments()

        if last_submission and last_submission.comments:
            self._comments_pane.load_comments(last_submission.comments)
            self._comments_dock.show()
        else:
            self._comments_dock.hide()
