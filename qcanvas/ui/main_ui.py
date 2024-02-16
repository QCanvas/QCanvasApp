from abc import ABC, abstractmethod
from asyncio import Semaphore, Lock, Event
from datetime import datetime
from typing import Sequence, TypeVar, Generic

from qasync import asyncSlot

from qcanvas.QtVersionHelper.QtGui import QStandardItemModel, QStandardItem
from qcanvas.QtVersionHelper.QtWidgets import *
from qcanvas.QtVersionHelper.QtCore import QItemSelection, Slot, Signal, QStringListModel, Qt, QModelIndex, \
    QItemSelectionModel

import qcanvas.db.database as db
from qcanvas.ui.container_item import ContainerItem
from qcanvas.util import canvas_garbage_remover
from qcanvas.util.course_indexer import CourseLoader
from qcanvas.util.file_lister import file_list
from qcanvas.util.file_lister.file_list import PageResourceModel

default_assignments_module_names = ["assessments", "assessment"]

T = TypeVar("T")


class PageLikeViewer(QWidget, Generic[T]):
    def __init__(self):
        super().__init__()
        self.viewer = QTextBrowser()
        self.tree = QTreeView()
        self.model = QStandardItemModel()

        self.tree.setModel(self.model)
        self.tree.selectionModel().selectionChanged.connect(self.on_item_clicked)

        layout = QHBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.viewer)

        layout.setStretch(1, 1)

        self.setLayout(layout)

    @abstractmethod
    def fill_tree(self, data: T):
        ...

    @Slot(QItemSelection, QItemSelection)
    def on_item_clicked(self, selected: QItemSelection, deselected: QItemSelection):
        if len(selected.indexes()) == 0:
            self.viewer.clear()
            return

        node = self.model.itemFromIndex(selected.indexes()[0])

        if isinstance(node, ContainerItem):
            item = node.content

            if isinstance(item, db.PageLike):
                if item.content is None:
                    return

                self.viewer.setHtml(canvas_garbage_remover.remove_stylesheets_from_html(item.content))


class PagesViewer(PageLikeViewer[db.Course]):

    def fill_tree(self, course: db.Course):
        self.model.clear()

        root = self.model.invisibleRootItem()

        for module in course.modules:
            if module.name.lower() in default_assignments_module_names:
                continue

            module_node = ContainerItem(module)

            for module_item in list[db.ModuleItem](module.items):
                module_node.appendRow(ContainerItem(module_item))

            root.appendRow(module_node)

        self.model.setHorizontalHeaderLabels(["Pages"])
        self.tree.expandAll()

class AssignmentsViewer(PageLikeViewer[db.Course]):

    def fill_tree(self,  course: db.Course):
        self.model.clear()

        root = self.model.invisibleRootItem()

        default_assessments_module = None

        for module in course.modules:
            if module.name.lower() in default_assignments_module_names:
                default_assessments_module = module
                break

        if default_assessments_module is not None:
            for module_item in default_assessments_module.items:
                root.appendRow(ContainerItem(module_item))
            for assignment in course.assignments:
                root.appendRow(ContainerItem(assignment))

        self.model.setHorizontalHeaderLabels(["Putting the ASS in assignments"])
        self.tree.expandAll()


class AppMainWindow(QMainWindow):
    loaded = Signal()
    operation_lock = Event()
    courses: Sequence[db.Course] = []

    def __init__(self, data_loader: CourseLoader):
        super().__init__()

        self.setWindowTitle("QCanvas (Under construction)")

        right_splitter = QSplitter()
        right_splitter.setOrientation(Qt.Orientation.Vertical)

        self.loader = data_loader

        self.file_tree, self.file_tree_model = self.setup_file_tree()
        self.assignment_file_tree, self.assignment_file_tree_model = self.setup_file_tree()

        file_view_layout = QHBoxLayout()
        file_view_layout.addWidget(self.setup_file_column("Files", self.file_tree))
        file_view_layout.addWidget(self.setup_file_column("Assignment Files", self.assignment_file_tree))

        file_view = QWidget()
        file_view.setLayout(file_view_layout)

        self.page_viewer = QTextBrowser()

        self.sync_button = QPushButton("Synchronize")
        self.sync_button.clicked.connect(self.sync_data)

        self.course_selector = QTreeView()
        self.course_selector_model = QStandardItemModel()
        self.course_selector.setModel(self.course_selector_model)
        self.course_selector.selectionModel().selectionChanged.connect(self.on_item_clicked)

        self.tab_widget = QTabWidget()
        self.assignment_viewer = AssignmentsViewer()
        self.pages_viewer = PagesViewer()

        self.tab_widget.insertTab(0, file_view, "Files")
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

    @staticmethod
    def setup_file_column(name : str, file_tree : QWidget) -> QWidget:
        gbox = QGroupBox(name)
        layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        layout.addWidget(file_tree)
        gbox.setLayout(layout)

        return gbox



    @staticmethod
    def setup_file_tree():
        file_tree = QTreeView()
        file_tree_model = PageResourceModel()
        file_tree.setModel(file_tree_model)
        file_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        file_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        file_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        file_tree.header().setStretchLastSection(0)
        file_tree.setItemDelegateForColumn(3, file_list.PageResourceDelegate())
        file_tree.setAlternatingRowColors(True)

        return file_tree, file_tree_model

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
            return

        node = self.course_selector_model.itemFromIndex(selected.indexes()[0])

        if isinstance(node, ContainerItem):
            item = node.content

            if isinstance(item, db.Course):
                self.pages_viewer.fill_tree(item)
                self.assignment_viewer.fill_tree(item)

                # fixme this does not move assignment pages from the default assignment module into the assignments column
                # todo make this not stupid
                self.file_tree_model.update_page_list([x for x in item.module_items if x.module.name.lower() not in default_assignments_module_names])
                self.file_tree.expandAll()

                self.assignment_file_tree_model.update_page_list(item.assignments + [x for x in item.module_items if x.module.name.lower() in default_assignments_module_names])
                self.assignment_file_tree.expandAll()
