import logging

import qcanvas_backend.database.types as db
from qtpy.QtCore import Slot
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.page_tree import PageTree
from qcanvas.util.layouts import layout

_logger = logging.getLogger(__name__)


class CourseViewer(QWidget):
    def __init__(self, course: db.Course):
        super().__init__()

        self._text_viewer = QTextBrowser()
        self._page_tree = PageTree(course)
        self._page_tree.page_selected.connect(self._page_selected)
        self.setLayout(layout(QHBoxLayout, self._page_tree, self._text_viewer))
        self._page_tree.reexpand()

    @Slot()
    def _page_selected(self, page: db.ModulePage):
        if page is not None:
            _logger.debug("Show page %s", page.name)
            self._text_viewer.setPlainText(page.body)
