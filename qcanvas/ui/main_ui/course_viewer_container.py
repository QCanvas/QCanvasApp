import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qcanvas_backend.qcanvas import QCanvas
from qtpy.QtCore import Qt
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.course_viewer import CourseViewer

_logger = logging.getLogger(__name__)


class CourseViewerContainer(QStackedWidget):
    # FIXME REMOVE qcanvas
    def __init__(self, qcanvas: QCanvas):
        super().__init__()
        self._qcanvas = qcanvas
        self._course_viewers: dict[str, CourseViewer] = {}
        self._last_course_id: Optional[str] = None
        self._placeholder = QLabel("No Course Selected")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self._placeholder)

    def show_blank(self):
        self._last_course_id = None
        self.setCurrentWidget(self._placeholder)

    def load_course(self, course: db.Course) -> None:
        if course.id not in self._course_viewers:
            viewer = CourseViewer(
                course=course,
                resource_manager=self._qcanvas.resource_manager,
            )
            self._course_viewers[course.id] = viewer
            self.addWidget(viewer)
        else:
            viewer = self._course_viewers[course.id]

        self.setCurrentWidget(viewer)
        self._last_course_id = course.id

    async def reload_all(self, *, sync_receipt: Optional[SyncReceipt]) -> None:
        raise NotImplementedError()

    #     courses = (await self._qcanvas.get_data()).courses
    #     for course in courses:
    #         if course.id in self._course_viewers:
    #             viewer = self._course_viewers[course.id]
    #             viewer.reload(course)
