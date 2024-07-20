import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt

from qcanvas.ui.course_viewer.tabs.content_tab import ContentTab
from qcanvas.ui.course_viewer.tabs.page_tab.page_tree import PageTree

_logger = logging.getLogger(__name__)


class PageTab(ContentTab):

    @staticmethod
    def create_from_receipt(
        *,
        course: db.Course,
        sync_receipt: Optional[SyncReceipt],
        downloader: ResourceManager,
    ) -> "PageTab":
        return PageTab(course=course, sync_receipt=sync_receipt, downloader=downloader)

    def __init__(
        self,
        *,
        course: db.Course,
        sync_receipt: Optional[SyncReceipt],
        downloader: ResourceManager,
    ):
        super().__init__(
            explorer=PageTree.create_from_receipt(course, sync_receipt=sync_receipt),
            title_placeholder_text="No page selected",
            downloader=downloader,
        )
