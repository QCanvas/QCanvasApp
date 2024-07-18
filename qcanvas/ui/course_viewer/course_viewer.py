import logging

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.tabs.pages_tab import PagesTab
from qcanvas.util.basic_fonts import bold_font
from qcanvas.util.layouts import layout

_logger = logging.getLogger(__name__)


class CourseViewer(QWidget):
    def __init__(self, course: db.Course, resource_manager: ResourceManager):
        super().__init__()

        self._course_label = QLabel(course.name)
        self._course_label.setFont(bold_font)
        self._tabs = QTabWidget()

        self._tabs.addTab(QLabel("Not implemented"), "Files")
        self._tabs.addTab(PagesTab(course, resource_manager), "Pages")
        self._tabs.addTab(QLabel("Not implemented"), "Assignments")
        self._tabs.addTab(QLabel("Not implemented"), "Mail")
        # self._tabs.addTab(QLabel("Not implemented"), "Panopto") The meme lives on!

        self.setLayout(layout(QVBoxLayout, self._course_label, self._tabs))
