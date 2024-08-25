import logging
from math import floor
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt, empty_receipt
from qtpy.QtCore import Qt, Slot
from qtpy.QtWidgets import *

from qcanvas import icons
from qcanvas.ui.course_viewer.course_viewer import CourseViewer
from qcanvas.util import themes

_logger = logging.getLogger(__name__)


class _PlaceholderLogo(QLabel):
    """
    Automatically resizing logo icon for when no course is selected
    """

    def __init__(self):
        super().__init__()
        self._icon = icons.branding.logo_transparent
        self._old_width = -1
        self._old_height = -1
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        # Because we are using a pixmap for the icon, it will not get updated like a normal QIcon when the theme changes,
        # So we need to update it ourselves
        themes.theme_changed().connect(self._theme_changed)

    def resizeEvent(self, event) -> None:
        self._update_image()

    @Slot()
    def _theme_changed(self) -> None:
        self._update_image(force=True)

    def _update_image(self, force: bool = False) -> None:
        # Calculate the size of the logo as half of the width/height with a max size of 1000x1000
        width = min(floor(self.width() * 0.5), 500)
        height = min(floor(self.height() * 0.5), 500)

        if force or (width != self._old_width and height != self._old_height):
            self._old_width = width
            self._old_height = height
            self.setPixmap(self._icon.pixmap(width, height))


class CourseViewerContainer(QStackedWidget):
    def __init__(self, downloader: ResourceManager):
        super().__init__()
        self._course_viewers: dict[str, CourseViewer] = {}
        self._downloader = downloader
        self._last_course_id: Optional[str] = None
        self._selected_course: Optional[db.Course] = None
        self._last_sync_receipt: SyncReceipt = empty_receipt()
        self._placeholder = _PlaceholderLogo()
        self.addWidget(self._placeholder)

    def show_blank(self) -> None:
        self._last_course_id = None
        self._selected_course = None
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
        self._selected_course = course
        self._last_course_id = course.id

    async def reload_all(
        self, courses: Sequence[db.Course], *, sync_receipt: SyncReceipt
    ) -> None:
        self._last_sync_receipt = sync_receipt
        for course in courses:
            if course.id in self._course_viewers:
                viewer = self._course_viewers[course.id]
                viewer.reload(course, sync_receipt=sync_receipt)

    @property
    def selected_course(self) -> Optional[db.Course]:
        return self._selected_course
