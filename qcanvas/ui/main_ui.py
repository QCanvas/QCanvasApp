from dataclasses import dataclass
from typing import Sequence

from qcanvas.QtVersionHelper.QtGui import QStandardItemModel, QStandardItem
from qcanvas.QtVersionHelper.QtWidgets import QMainWindow, QTreeView
from qcanvas.QtVersionHelper.QtCore import Qt

import qcanvas.util.tree_util as tree

import qcanvas.db.database as db
# from qcanvas.ui.course_model import CourseModel
from qcanvas.util.tree_util import ExpandingTreeView


class MyItem(QStandardItem):
    _data: tree.HasText

    def __init__(self, data: tree.HasText):
        super().__init__()
        self._data = data

    def data(self, role=257):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data.text


class AppMainWindow(QMainWindow):
    def __init__(self, courses: Sequence[db.Course]):
        super().__init__()

        model = QStandardItemModel()

        root: QStandardItem = model.invisibleRootItem()

        for course in courses:
            course_node = MyItem(course)

            default_assessments_module : db.Module | None = None

            for module in course.modules:
                if module.name.lower() in ["assessments", "assessment"]:
                    default_assessments_module = module
                    continue

                module_node = MyItem(module)

                for module_item in list[db.ModuleItem](module.items):
                    module_item_node = MyItem(module_item)

                    for resource in module_item.resources:
                        module_item_node.appendRow(MyItem(resource))

                    module_node.appendRow(module_item_node)

                course_node.appendRow(module_node)

            if default_assessments_module is not None:
                assignments_node = QStandardItem()

                assignments_node.setText("Putting the ASS in assignments")

                for module_item in default_assessments_module.items:
                    page_node = MyItem(module_item)

                    for resource in module_item.resources:
                        page_node.appendRow(MyItem(resource))

                    assignments_node.appendRow(page_node)

                for assignment in course.assignments:
                    assignment_node = MyItem(assignment)

                    for resource in assignment.resources:
                        assignment_node.appendRow(MyItem(resource))

                    assignments_node.appendRow(assignment_node)

                course_node.appendRow(assignments_node)

            root.appendRow(course_node)

        self.tree = QTreeView()
        self.tree.setModel(model)
        self.setCentralWidget(self.tree)
