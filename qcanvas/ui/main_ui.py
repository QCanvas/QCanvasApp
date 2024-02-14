import dataclasses
from asyncio import Semaphore, Lock, Event
from datetime import datetime
from qasync import asyncSlot

from qcanvas.QtVersionHelper.QtGui import QStandardItemModel, QStandardItem
from qcanvas.QtVersionHelper.QtWidgets import *
from qcanvas.QtVersionHelper.QtCore import QItemSelection, Slot, Signal, QStringListModel, Qt

import qcanvas.db.database as db
from qcanvas.ui.container_item import ContainerItem
from qcanvas.util import canvas_garbage_remover
from qcanvas.util.course_indexer import CourseLoader
from qcanvas.util.file_lister import file_list
from qcanvas.util.file_lister.file_list import PageResourceModel


class AppMainWindow(QMainWindow):
    loaded = Signal()
    operation_lock = Event()

    def __init__(self, data_loader: CourseLoader):
        super().__init__()

        stack_panel = QVBoxLayout()
        centre_splitter = QSplitter()

        right_splitter = QSplitter()
        right_splitter.setOrientation(Qt.Orientation.Vertical)

        self.loader = data_loader

        self.course_tree = QTreeView()
        self.course_tree_model = QStandardItemModel()
        self.course_tree.setModel(self.course_tree_model)
        self.course_tree.selectionModel().selectionChanged.connect(self.on_item_clicked)

        self.file_tree = QTreeView()
        self.file_tree_model = PageResourceModel()
        self.file_tree.setModel(self.file_tree_model)
        self.file_tree.header().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.file_tree.setItemDelegate(file_list.PageResourceDelegate())
        self.file_tree.setAlternatingRowColors(True)

        self.page_viewer = QTextBrowser()

        self.sync_button = QPushButton("Synchronize")
        self.sync_button.clicked.connect(self.sync_data)

        right_splitter.addWidget(self.file_tree)
        right_splitter.addWidget(self.page_viewer)

        centre_splitter.addWidget(self.course_tree)
        centre_splitter.addWidget(right_splitter)

        stack_panel.addWidget(centre_splitter)
        stack_panel.addWidget(self.sync_button)

        central_widget = QWidget()
        central_widget.setLayout(stack_panel)
        self.setCentralWidget(central_widget)

        self.loaded.connect(self.load_data)
        self.loaded.emit()

    @asyncSlot()
    async def sync_data(self):

        # self.operation_lock.
        self.sync_button.setEnabled(False)
        self.sync_button.setText("Synchronizing")
        try:
            await self.loader.synchronize_with_canvas()
            await self.load_data()
        finally:
            self.sync_button.setEnabled(True)
            self.sync_button.setText("Synchronize")

    @asyncSlot()
    async def load_data(self):
        self.course_tree_model.clear()

        self.course_tree_model.setHorizontalHeaderItem(0, QStandardItem("Course"))

        root: QStandardItem = self.course_tree_model.invisibleRootItem()
        courses = sorted(await self.loader.get_data(), key=lambda x: x.term.start_at or datetime.min)

        for course in courses:
            course_node = ContainerItem(course)

            default_assessments_module: db.Module | None = None

            for module in course.modules:
                if module.name.lower() in ["assessments", "assessment"]:
                    default_assessments_module = module
                    continue

                module_node = ContainerItem(module)

                for module_item in list[db.ModuleItem](module.items):
                    module_node.appendRow(ContainerItem(module_item))

                course_node.appendRow(module_node)

            if default_assessments_module is not None:
                assignments_node = QStandardItem()

                assignments_node.setText("Putting the ASS in assignments")

                for module_item in default_assessments_module.items:
                    assignments_node.appendRow(ContainerItem(module_item))

                for assignment in course.assignments:
                    assignments_node.appendRow(ContainerItem(assignment))

                course_node.appendRow(assignments_node)

            root.appendRow(course_node)

    @Slot(QItemSelection, QItemSelection)
    def on_item_clicked(self, selected: QItemSelection, deselected: QItemSelection):
        node = self.course_tree_model.itemFromIndex(selected.indexes()[0])

        if isinstance(node, ContainerItem):
            item = node.content

            if isinstance(item, db.PageLike):
                if item.content is None:
                    return

                self.file_tree_model.update_page_list([item])
                self.file_tree.expandAll()

                self.page_viewer.setHtml(canvas_garbage_remover.remove_stylesheets_from_html(item.content))
            elif isinstance(item, db.Course):
                self.file_tree_model.update_page_list(item.module_items)
                self.file_tree.expandAll()
