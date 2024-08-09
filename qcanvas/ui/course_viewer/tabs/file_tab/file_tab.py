import logging

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.file_tab.pages_file_tree import PagesFileTree
from qcanvas.util.layouts import layout

_logger = logging.getLogger(__name__)


class FileTab(QWidget):
    @staticmethod
    def create_from_receipt(
        *,
        course: db.Course,
        sync_receipt: SyncReceipt,
        downloader: ResourceManager,
    ) -> "FileTab":
        return FileTab(course=course, sync_receipt=sync_receipt, downloader=downloader)

    def __init__(
        self,
        course: db.Course,
        downloader: ResourceManager,
        *,
        sync_receipt: SyncReceipt = None,
    ):
        super().__init__()

        self._page_file_tree = PagesFileTree.create_from_receipt(
            course, sync_receipt=sync_receipt, resource_manager=downloader
        )
        # self._assignment_file_tree = FileTree.create_from_receipt(
        #     course,
        #     sync_receipt=sync_receipt,
        #     mode="assignments",
        #     resource_manager=downloader,
        # )

        self.setLayout(layout(QHBoxLayout, self._page_file_tree))

    def reload(self, course: db.Course, *, sync_receipt: SyncReceipt) -> None:
        pass
