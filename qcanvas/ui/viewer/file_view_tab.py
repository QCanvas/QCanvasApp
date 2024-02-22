from typing import Sequence

from PySide6.QtWidgets import *  # QWidget, QTreeView, QGroupBox, QBoxLayout, QHeaderView, QHBoxLayout, QComboBox, QLabel

import qcanvas.db as db
from qcanvas.ui.viewer.file_list import FileList
from qcanvas.util.constants import default_assignments_module_names
from qcanvas.util.download_pool import DownloadPool


class FileColumn(QGroupBox):
    def __init__(self, column_name, download_pool: DownloadPool):
        super().__init__(title=column_name)

        self.tree = FileList(download_pool)
        self.setLayout(QBoxLayout(QBoxLayout.Direction.TopToBottom))
        self.layout().addWidget(self.tree)

    def load_items(self, items: Sequence[db.ModuleItem | db.Module]):
        self.tree.load_items(items)

    def clear(self):
        self.tree.clear()


class FileViewTab(QWidget):

    def __init__(self, download_pool: DownloadPool):
        super().__init__()

        self.files_column = FileColumn("Files", download_pool)
        self.assignment_files_column = FileColumn("Assignment files", download_pool)

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

        if course.preferences.files_group_by_preference == db.GroupByPreference.GROUP_BY_MODULES:
            exclude_assignments_module = list(
                filter(lambda x: x.name.lower() not in default_assignments_module_names, course.modules))

            self.files_column.load_items(exclude_assignments_module)
        else:
            self.files_column.load_items(module_items)

        self.assignment_files_column.load_items(assignment_items + course.assignments)

    def clear(self):
        self.files_column.clear()
        self.assignment_files_column.clear()
