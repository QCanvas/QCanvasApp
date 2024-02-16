from typing import Sequence

from qcanvas.QtVersionHelper.QtWidgets import QWidget, QTreeView, QGroupBox, QBoxLayout, QHeaderView, QHBoxLayout
from qcanvas.ui.viewer.file_list import FileColumnModel, FileColumnDelegate

import qcanvas.db as db
from qcanvas.util.constants import default_assignments_module_names


class FileColumn(QGroupBox):


    def __init__(self, column_name):
        super().__init__(title=column_name)

        self.tree = QTreeView()
        self.model = FileColumnModel()

        self.tree.setModel(self.model)
        self.tree.setItemDelegateForColumn(3, FileColumnDelegate(self.tree))
        self.tree.setAlternatingRowColors(True)

        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(0)

        self.setLayout(QBoxLayout(QBoxLayout.Direction.TopToBottom))
        self.layout().addWidget(self.tree)

    def load_page_list(self, pages: Sequence[db.ModuleItem]):
        self.model.load_page_list(pages)
        self.tree.expandAll()


class FileViewTab(QWidget):
    def __init__(self):
        super().__init__()

        self.files_column = FileColumn("Files")
        self.assignment_files_column = FileColumn("Assignment files")

        layout = QHBoxLayout()
        layout.addWidget(self.files_column)
        layout.addWidget(self.assignment_files_column)

        self.setLayout(layout)

    def load_course_files(self, course: db.Course):
        module_items: list[db.ModuleItem] = []
        assignment_items: list[db.ModuleItem] = []

        for module_item in course.module_items:
            if module_item.module.name.lower() in default_assignments_module_names:
                assignment_items.append(module_item)
            else:
                module_items.append(module_item)

        self.files_column.load_page_list(module_items)
        self.assignment_files_column.load_page_list(assignment_items + course.assignments)
