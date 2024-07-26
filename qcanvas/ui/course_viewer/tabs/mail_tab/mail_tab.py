import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.content_tab import ContentTab
from qcanvas.ui.course_viewer.tabs.mail_tab.mail_tree import MailTree
from qcanvas.ui.course_viewer.tabs.util import date_strftime_format
from qcanvas.util.basic_fonts import bold_label
from qcanvas.util.layouts import grid_layout

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

    def setup_info_grid(self) -> QGridLayout:
        grid = grid_layout(
            [
                [
                    bold_label("From:"),
                    self._sender_label,
                ],
                [
                    bold_label("Date:"),
                    self._date_sent_label,
                ],
            ]
        )

        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)

        return grid

    def update_info_grid(self, mail: db.CourseMessage) -> None:
        self._date_sent_label.setText(mail.creation_date.strftime(date_strftime_format))
        self._sender_label.setText(mail.sender_name)
