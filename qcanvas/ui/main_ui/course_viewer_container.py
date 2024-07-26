import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt, empty_receipt
from qtpy.QtCore import Qt
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.course_viewer import CourseViewer

_logger = logging.getLogger(__name__)


class CourseViewerContainer(QStackedWidget):
    def __init__(self, downloader: ResourceManager):
        super().__init__()
        self._course_viewers: dict[str, CourseViewer] = {}
        self._downloader = downloader
        self._last_course_id: Optional[str] = None
        self._last_sync_receipt: SyncReceipt = empty_receipt()
        self._placeholder = QLabel("No Course Selected")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self._placeholder)

    def show_blank(self) -> None:
        self._last_course_id = None
        self.setCurrentWidget(self._placeholder)

    def load_course(self, course: db.Course) -> None:
        if course.id not in self._course_viewers:
            viewer = CourseViewer(
                course=course,
                downloader=self._downloader,
                sync_receipt=self._last_sync_receipt,
            )
            self._course_viewers[course.id] = viewer
            self.addWidget(viewer)
        else:
            viewer = self._course_viewers[course.id]

        self.setCurrentWidget(viewer)
        self._last_course_id = course.id

    async def reload_all(
        self, courses: Sequence[db.Course], *, sync_receipt: SyncReceipt
    ) -> None:
        self._last_sync_receipt = sync_receipt
        for course in courses:
            if course.id in self._course_viewers:
                viewer = self._course_viewers[course.id]
                viewer.reload(course, sync_receipt=sync_receipt)
