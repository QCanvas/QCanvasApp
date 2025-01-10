import logging

from libqcanvas import db
from libqcanvas.net.resources.download.resource_manager import ResourceManager
from libqcanvas.net.sync.sync_receipt import SyncReceipt
from libqcanvas.util import as_local
from PySide6.QtWidgets import QLabel, QLayout

from qcanvas.ui.course_viewer.tabs.content_tab import ContentTab
from qcanvas.ui.course_viewer.tabs.mail_tab.mail_tree import MailTree
from qcanvas.ui.course_viewer.tabs.constants import date_strftime_format
import qcanvas.util.ui_tools as ui

_logger = logging.getLogger(__name__)


# todo maybe update has_been_read? probably not the responsibility of this class though
class MailTab(ContentTab):
    def __init__(
        self,
        *,
        course: db.Course,
        sync_receipt: SyncReceipt,
        downloader: ResourceManager,
    ):
        super().__init__(
            explorer=MailTree.create_from_receipt(course, sync_receipt=sync_receipt),
            title_placeholder_text="No mail selected",
            downloader=downloader,
        )

        self._date_sent_label = QLabel("")
        self._sender_label = QLabel("")

        self.enable_info_grid()

    def setup_info_grid(self) -> QLayout:
        return ui.form_layout(
            {"From": self._sender_label, "Date": self._date_sent_label},
        )

    def update_info_grid(self, mail: db.Message) -> None:
        self._date_sent_label.setText(
            as_local(mail.creation_date).strftime(date_strftime_format)
        )
        self._sender_label.setText(mail.sender_name)
