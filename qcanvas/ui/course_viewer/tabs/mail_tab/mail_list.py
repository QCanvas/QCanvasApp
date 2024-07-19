import logging
from typing import *

from qtpy.QtCore import Slot
from qtpy.QtCore import Signal
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtWidgets import *
import qcanvas_backend.database.types as db

from qcanvas.ui.memory_tree import MemoryTreeWidget, MemoryTreeWidgetItem
from qcanvas.util.basic_fonts import bold_font, normal_font

_logger = logging.getLogger(__name__)


class MailList(MemoryTreeWidget):
    mail_selected = Signal(db.CourseMessage)

    def __init__(
        self,
        course: db.Course,
        *,
        initial_sync_receipt: Optional[SyncReceipt],
    ):
        super().__init__(f"course.{course.id}.mail")
        self._course = course
        self._last_selected_id: Optional[str] = None

        self.setHeaderLabels(["Subject", "From"])
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setStretchLastSection(False)

        self._add_items(initial_sync_receipt)
        self.selectionModel().selectionChanged.connect(self._selection_changed)

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]) -> None:
        self._course = course
        self._add_items(sync_receipt)

        # todo all these things should be their own function
        if self._last_selected_id is not None:
            if not self.select_ids([self._last_selected_id]):
                self._last_selected_id = None

    def _add_items(self, sync_receipt: Optional[SyncReceipt]) -> None:
        self.clear()

        widgets = []
        for message in self._course.messages:  # type: db.CourseMessage
            message_widget = MemoryTreeWidgetItem(
                id=message.id,
                data=message,
                strings=[message.name, message.sender_name],
            )

            if sync_receipt is not None and message.id in sync_receipt.updated_messages:
                message_widget.setFont(0, bold_font)

            widgets.append(message_widget)

        self.addTopLevelItems(widgets)

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

        if isinstance(selected.extra_data, db.CourseMessage):
            self.mail_selected.emit(selected.extra_data)
            self._last_selected_id = selected.extra_data.id
        else:
            # Should be impossible to get here
            self.mail_selected.emit(None)
            self._last_selected_id = None
