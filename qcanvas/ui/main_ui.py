from typing import Sequence

from qcanvas.QtVersionHelper import QtWidgets
import qcanvas.db.database as db
from qcanvas.ui.course_model import CourseModel
from qcanvas.util.tree_util import ExpandingTreeView


class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self, courses: Sequence[db.Course]):
        super().__init__()

        self.tree = ExpandingTreeView(None)
        self.tree_model = CourseModel(courses)
        self.tree.setModel(self.tree_model)
        self.setCentralWidget(self.tree)
