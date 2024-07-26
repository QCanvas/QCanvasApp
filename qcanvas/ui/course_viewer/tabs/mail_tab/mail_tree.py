import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.content_tree import ContentTree
from qcanvas.ui.memory_tree import MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class MailTree(ContentTree[db.Course]):

    def __init__(self, course_id: str):
        super().__init__(
            tree_name=f"course.{course_id}.mail",
            emit_selection_signal_for_type=db.CourseMessage,
        )
        self.ui_setup(
            header_text=["Subject", "Sender"],
            max_width=500,
            min_width=300,
            indentation=20,
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

        for message in course.messages:  # type: db.CourseMessage
            message_widget = self._create_mail_widget(message, sync_receipt)
            widgets.append(message_widget)

        return widgets

    def _create_mail_widget(
        self, message: db.CourseMessage, sync_receipt: SyncReceipt
    ) -> MemoryTreeWidgetItem:
        message_widget = MemoryTreeWidgetItem(
            id=message.id,
            data=message,
            strings=[message.name, message.sender_name],
        )

        if sync_receipt.was_updated(message):
            self.mark_as_unseen(message_widget)

        return message_widget
