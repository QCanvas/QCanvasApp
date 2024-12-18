import logging

from libqcanvas import db
from libqcanvas.net.resources.download.resource_manager import ResourceManager
from libqcanvas.net.sync.sync_receipt import SyncReceipt

from qcanvas.ui.course_viewer.tabs.content_tab import ContentTab
from qcanvas.ui.course_viewer.tabs.page_tab.page_tree import PageTree

_logger = logging.getLogger(__name__)


class PageTab(ContentTab):
    def __init__(
        self,
        *,
        course: db.Course,
        sync_receipt: SyncReceipt,
        downloader: ResourceManager,
    ):
        super().__init__(
            explorer=PageTree.create_from_receipt(course, sync_receipt=sync_receipt),
            title_placeholder_text="No page selected",
            downloader=downloader,
        )
