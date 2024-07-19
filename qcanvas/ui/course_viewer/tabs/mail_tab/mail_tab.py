import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Slot
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.mail_tab.mail_list import MailList
from qcanvas.ui.course_viewer.tabs.resource_rich_browser import ResourceRichBrowser
from qcanvas.util.layouts import layout

_logger = logging.getLogger(__name__)


# todo show date and subject of the mail in a label somewhere
# todo maybe update has_been_read? probably not the responsibility of this class though
class MailTab(QWidget):
    def __init__(
        self,
        course: db.Course,
        resource_manager: ResourceManager,
        *,
        initial_sync_receipt: Optional[SyncReceipt] = None
    ):
        super().__init__()
        self._viewer = ResourceRichBrowser(resource_manager)
        self._mail_list = MailList(course, initial_sync_receipt=initial_sync_receipt)
        self.setLayout(layout(QHBoxLayout, self._mail_list, self._viewer))
        self._mail_list.mail_selected.connect(self._mail_selected)

    def reload(self, course: db.Course, *, sync_receipt: Optional[SyncReceipt]) -> None:
        self._mail_list.reload(course, sync_receipt=sync_receipt)

    @Slot()
    def _mail_selected(self, mail: db.CourseMessage):
        self._viewer.show_content(mail)
