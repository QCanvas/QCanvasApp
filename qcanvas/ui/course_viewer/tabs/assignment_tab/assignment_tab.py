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
from qcanvas.ui.qml_components import CommentsPane, AttachmentsPane
from qcanvas.ui.course_viewer.tabs.content_tab import ContentTab
from qcanvas.ui.course_viewer.tabs.constants import (
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

        # fixme: can't figure out how to get the panes to have the right size without showing them when nothing is selected
        self._comments_pane = CommentsPane(downloader)
        self._comments_dock = ui.dock_widget(
            title="Comments",
            name="comments_dock",
            widget=self._comments_pane,
            min_size=ui.size(150, 150),
            features=QDockWidget.DockWidgetFeature.DockWidgetMovable,
            hide=False,
        )

        self._submission_files_pane = AttachmentsPane(downloader)
        self._submission_files_dock = ui.dock_widget(
            title="Submission Files",
            name="sub_files_dock",
            widget=self._submission_files_pane,
            min_size=ui.size(150, 150),
            features=QDockWidget.DockWidgetFeature.DockWidgetMovable,
            hide=False,
        )

        self._main_container.setCentralWidget(self._viewer)
        self._main_container.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea, self._submission_files_dock
        )
        self._main_container.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea, self._comments_dock
        )

        self._main_container.resizeDocks(
            [self._submission_files_dock, self._comments_dock],
            [350, 350],
            Qt.Orientation.Horizontal,
        )
        self._main_container.resizeDocks(
            [self._submission_files_dock],
            [200],
            Qt.Orientation.Vertical,
        )

        self._due_date_label = QLabel("")
        self._score_label = QLabel("")
        self.enable_info_grid()

    @override
    def _setup_layout(self) -> None:
        super()._setup_layout()
        self.content_grid.replaceWidget(
            self._viewer,
            self._main_container,
        )

        self.content_grid.setColumnStretch(0, 1)
        self.content_grid.setColumnStretch(1, 3)

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

        self._score_label.setText(
            f"<b>{submission_score}</b>/{assignment.max_score or '?'}"
        )

        if last_submission and last_submission.attachments:
            self._submission_files_pane.load_files(last_submission.attachments)
            self._submission_files_dock.show()
        else:
            self._submission_files_pane.clear_files()
            self._submission_files_dock.hide()

        if last_submission and last_submission.comments:
            self._comments_pane.load_comments(last_submission.comments)
            self._comments_dock.show()
        else:
            self._comments_pane.clear_comments()
            self._comments_dock.hide()

    @override
    def _show_blank(self) -> None:
        super()._show_blank()

        self._comments_dock.hide()
        self._submission_files_dock.hide()
