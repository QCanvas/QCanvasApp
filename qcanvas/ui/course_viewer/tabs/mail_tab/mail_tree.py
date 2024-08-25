import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtWidgets import *

from qcanvas import icons
from qcanvas.ui.course_viewer.content_tree import ContentTree
from qcanvas.ui.course_viewer.tree_widget_data_item import TreeWidgetDataItem

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
            alternating_row_colours=True,
        )

        self.set_columns_resize_mode(
            [QHeaderView.ResizeMode.Stretch, QHeaderView.ResizeMode.ResizeToContents]
        )

    def create_tree_items(
        self, course: db.Course, sync_receipt: SyncReceipt
    ) -> Sequence[TreeWidgetDataItem]:
        widgets = []

        for message in course.messages:  # type: db.CourseMessage
            message_widget = self._create_mail_widget(message, sync_receipt)
            message_widget.setIcon(0, icons.tree_items.mail)
            widgets.append(message_widget)

        return widgets

    def _create_mail_widget(
        self, message: db.CourseMessage, sync_receipt: SyncReceipt
    ) -> TreeWidgetDataItem:
        message_widget = TreeWidgetDataItem(
            id=message.id,
            data=message,
            strings=[message.name, message.sender_name],
        )

        if sync_receipt.was_updated(message):
            self.mark_as_unseen(message_widget)

        return message_widget
