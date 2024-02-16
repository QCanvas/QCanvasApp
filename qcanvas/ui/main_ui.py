from abc import abstractmethod
from asyncio import Event
from datetime import datetime
from typing import Sequence, TypeVar, Generic

from qasync import asyncSlot

from qcanvas.QtVersionHelper.QtGui import QStandardItemModel, QStandardItem
from qcanvas.QtVersionHelper.QtWidgets import *
from qcanvas.QtVersionHelper.QtCore import QItemSelection, Slot, Signal, Qt

import qcanvas.db.database as db
from qcanvas.ui.container_item import ContainerItem
from qcanvas.ui.viewer.file_view_tab import FileViewTab
from qcanvas.ui.viewer.page_list_viewer import AssignmentsViewer, PagesViewer
from qcanvas.util import canvas_garbage_remover
from qcanvas.util.constants import default_assignments_module_names
from qcanvas.util.course_indexer import CourseLoader
from qcanvas.ui.viewer import file_list
from qcanvas.ui.viewer.file_list import FileColumnModel

T = TypeVar("T")


class AppMainWindow(QMainWindow):
    loaded = Signal()
    operation_lock = Event()
    courses: Sequence[db.Course] = []

    def __init__(self, data_loader: CourseLoader):
        super().__init__()

        self.selected_course: db.Course | None = None

        self.setWindowTitle("QCanvas (Under construction)")

        right_splitter = QSplitter()
        right_splitter.setOrientation(Qt.Orientation.Vertical)

        self.loader = data_loader

        self.sync_button = QPushButton("Synchronize")
        self.sync_button.clicked.connect(self.sync_data)

        self.course_selector = QTreeView()
        self.course_selector_model = QStandardItemModel()
        self.course_selector.setModel(self.course_selector_model)
        self.course_selector.selectionModel().selectionChanged.connect(self.on_item_clicked)

        self.tab_widget = QTabWidget()
        self.assignment_viewer = AssignmentsViewer()
        self.pages_viewer = PagesViewer()

        self.file_viewer = FileViewTab()
        self.file_viewer.group_by_preference_changed.connect(self.course_file_group_by_preference_changed)

        self.tab_widget.insertTab(0, self.file_viewer, "Files")
        self.tab_widget.insertTab(1, self.assignment_viewer, "Assignments")
        self.tab_widget.insertTab(2, self.pages_viewer, "Pages")

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.course_selector)
        h_layout.addWidget(self.tab_widget)
        h_layout.setStretch(1, 1)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.sync_button)

        widget = QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

        self.loaded.connect(self.load_course_list)
        self.loaded.emit()

    @asyncSlot()
    async def sync_data(self):
        # # self.operation_lock.
        self.sync_button.setEnabled(False)
        self.sync_button.setText("Synchronizing")
        try:
            await self.loader.synchronize_with_canvas()
            await self.load_course_list()

        finally:
            self.sync_button.setEnabled(True)
            self.sync_button.setText("Synchronize")

    @staticmethod
    def group_courses_by_term(courses: Sequence[db.Course]):
        courses_grouped_by_term: dict[db.Term, list[db.Course]] = {}

        # Put courses into groups in the above dict
        for course in courses:
            if course.term in courses_grouped_by_term:
                courses_grouped_by_term[course.term].append(course)
            else:
                courses_grouped_by_term[course.term] = [course]

        # Convert the dict item list into a mutable list
        pairs = list(courses_grouped_by_term.items())
        # Sort them by start date, with most recent terms at the start
        pairs.sort(key=lambda x: x[0].start_at or datetime.min, reverse=True)

        return pairs

    @asyncSlot()
    async def load_course_list(self):
        self.courses = (await self.loader.get_data())

        self.selected_course = None
        self.course_selector_model.clear()
        self.course_selector_model.setHorizontalHeaderLabels(["Course"])

        courses_root = self.course_selector_model.invisibleRootItem()

        for term, courses in self.group_courses_by_term(self.courses):
            term_node = QStandardItem(term.name)

            for course in courses:
                term_node.appendRow(ContainerItem(course))

            courses_root.appendRow(term_node)

        self.course_selector.expandAll()

    @Slot(QItemSelection, QItemSelection)
    def on_item_clicked(self, selected: QItemSelection, deselected: QItemSelection):
        if len(selected.indexes()) == 0:
            self.selected_course = None
            return

        node = self.course_selector_model.itemFromIndex(selected.indexes()[0])

        if isinstance(node, ContainerItem):
            item = node.content

            if isinstance(item, db.Course):
                self.selected_course = item
                self.pages_viewer.fill_tree(item)
                self.assignment_viewer.fill_tree(item)
                self.file_viewer.load_course_files(item)
                return

        self.selected_course = None
        self.file_viewer.clear()

    @asyncSlot(db.CoursePreferences)
    async def course_file_group_by_preference_changed(self, preference: db.GroupByPreference):
        self.selected_course.preferences.files_group_by_preference = preference
        await self.loader.update_course_preferences(self.selected_course.preferences)
        self.file_viewer.load_course_files(self.selected_course)
