from typing import Sequence

from qcanvas.QtVersionHelper.QtGui import QAction, QActionGroup, create_qaction
from qcanvas.QtVersionHelper.QtCore import Signal, Qt, Slot, QPoint
from qcanvas.QtVersionHelper.QtWidgets import * #QWidget, QTreeView, QGroupBox, QBoxLayout, QHeaderView, QHBoxLayout, QComboBox, QLabel
from qcanvas.ui.viewer.file_list import FileList

import qcanvas.db as db
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
    group_by_preference_changed = Signal(db.GroupByPreference)

    def __init__(self, download_pool: DownloadPool):
        super().__init__()

        self.files_column = FileColumn("Files", download_pool)
        self.assignment_files_column = FileColumn("Assignment files", download_pool)

        self.group_by_combobox = QComboBox()

        self.group_by_preference: db.GroupByPreference | None = None
        self.group_preference_layout = QHBoxLayout()
        self.group_preference_layout.addWidget(QLabel("Group By:"))
        self.group_preference_layout.addWidget(self.group_by_combobox)
        self.group_preference_layout.setStretch(1, 1)

        widget = QWidget()
        widget.setLayout(self.group_preference_layout)

        # fixme this can't stay here
        self.files_column.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.files_column.customContextMenuRequested.connect(self.files_column_context_menu)

        self.group_by_preference_changed.connect(self.update_group_by_preferences)

        layout = QHBoxLayout()
        layout.addWidget(self.files_column)
        layout.addWidget(self.assignment_files_column)

        self.setLayout(layout)

    @Slot(db.GroupByPreference)
    def update_group_by_preferences(self, preference : db.GroupByPreference):
        if self.group_by_preference is not None:
            self.group_by_preference = preference

    def load_course_files(self, course: db.Course):
        self.group_by_preference = course.preferences.files_group_by_preference

        module_items: list[db.ModuleItem] = []
        assignment_items: list[db.ModuleItem] = []

        for module_item in course.module_items:
            if module_item.module.name.lower() in default_assignments_module_names:
                assignment_items.append(module_item)
            else:
                module_items.append(module_item)

        if self.group_by_preference == db.GroupByPreference.GROUP_BY_MODULES:
            exclude_assignments_module = list(filter(lambda x: x.name.lower() not in default_assignments_module_names, course.modules))

            self.files_column.load_items(exclude_assignments_module)
        else:
            self.files_column.load_items(module_items)

        self.assignment_files_column.load_items(assignment_items + course.assignments)

    def clear(self):
        self.group_by_preference = None
        self.files_column.clear()
        self.assignment_files_column.clear()

    @Slot(QPoint)
    def files_column_context_menu(self, pos: QPoint):
        if self.group_by_preference is None:
            return

        menu = QMenu(self.files_column)

        group_by_menu = menu.addMenu("Group by")

        select_group_preference_modules = create_qaction(
            name="Modules",
            checkable=True,
            checked=self.group_by_preference == db.GroupByPreference.GROUP_BY_MODULES,
            triggered=lambda: self.group_by_preference_changed.emit(db.GroupByPreference.GROUP_BY_MODULES)
        )

        select_group_preference_pages = create_qaction(
            name="Pages",
            checkable=True,
            checked=self.group_by_preference == db.GroupByPreference.GROUP_BY_PAGES,
            triggered=lambda: self.group_by_preference_changed.emit(db.GroupByPreference.GROUP_BY_PAGES)
        )

        action_group = QActionGroup(menu)
        action_group.addAction(select_group_preference_modules)
        action_group.addAction(select_group_preference_pages)

        group_by_menu.addAction(select_group_preference_pages)
        group_by_menu.addAction(select_group_preference_modules)

        menu.exec(self.files_column.mapToGlobal(pos))


