import logging
from asyncio import Event
from datetime import datetime
from typing import Sequence

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from qasync import asyncSlot

from qcanvas.QtVersionHelper.QtGui import QStandardItemModel, QStandardItem
from qcanvas.QtVersionHelper.QtWidgets import *
from qcanvas.QtVersionHelper.QtCore import QItemSelection, Slot, Signal, Qt, QModelIndex

import qcanvas.db.database as db
from qcanvas.ui.container_item import ContainerItem
from qcanvas.ui.viewer.file_list import FileRow
from qcanvas.ui.viewer.file_view_tab import FileViewTab
from qcanvas.ui.viewer.page_list_viewer import AssignmentsViewer, PagesViewer, LinkTransformer
from qcanvas.util.course_indexer import DataManager


class AppMainWindow(QMainWindow):
    logger = logging.getLogger()
    loaded = Signal()
    operation_lock = Event()

    def __init__(self, data_manager: DataManager):
        super().__init__()

        self.selected_course: db.Course | None = None
        self.courses: Sequence[db.Course] = []
        self.resources: dict[str, db.Resource] = {}
        self.data_manager = data_manager
        self.link_transformer = LinkTransformer(self.data_manager.link_scanners, self.resources)

        self.setWindowTitle("QCanvas (Under construction)")

        right_splitter = QSplitter()
        right_splitter.setOrientation(Qt.Orientation.Vertical)

        self.sync_button = QPushButton("Synchronize")
        self.sync_button.clicked.connect(self.sync_data)

        #todo just use QTreeWidget instead
        self.course_selector = QTreeView()
        self.course_selector_model = QStandardItemModel()
        self.course_selector.setModel(self.course_selector_model)
        self.course_selector.selectionModel().selectionChanged.connect(self.on_item_clicked)

        self.assignment_viewer = AssignmentsViewer(self.link_transformer)
        self.assignment_viewer.viewer.anchorClicked.connect(self.viewer_link_clicked)

        self.pages_viewer = PagesViewer(self.link_transformer)
        self.pages_viewer.viewer.anchorClicked.connect(self.viewer_link_clicked)

        self.file_viewer = FileViewTab(data_manager.download_pool)
        self.file_viewer.group_by_preference_changed.connect(self.course_file_group_by_preference_changed)

        self.file_viewer.files_column.tree.itemActivated.connect(self.download_file_from_file_pane)
        self.file_viewer.assignment_files_column.tree.itemActivated.connect(self.download_file_from_file_pane)

        self.tab_widget = QTabWidget()
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


    @asyncSlot(QUrl)
    async def viewer_link_clicked(self, url: QUrl):
        # The url of a transformed link will start with an '@'
        if url.toString().startswith(LinkTransformer.transformed_url_prefix):
            # The rest of the 'url' is just the file id
            resource = self.resources[url.toString().removeprefix(LinkTransformer.transformed_url_prefix)]

            await self.data_manager.download_resource(resource)
            QDesktopServices.openUrl(QUrl.fromLocalFile(resource.download_location.absolute()))


    @asyncSlot(QTreeWidgetItem, int)
    async def download_file_from_file_pane(self, item: QTreeWidgetItem, _ : int):
        if isinstance(item, FileRow):
            await self.data_manager.download_resource(item.resource)
            QDesktopServices.openUrl(QUrl.fromLocalFile(item.resource.download_location.absolute()))


    @asyncSlot()
    async def sync_data(self):
        # # self.operation_lock.
        self.sync_button.setEnabled(False)
        self.sync_button.setText("Synchronizing")
        try:
            await self.data_manager.synchronize_with_canvas()
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
        self.courses = (await self.data_manager.get_data())

        self.resources.clear()
        self.selected_course = None
        self.course_selector_model.clear()
        self.course_selector_model.setHorizontalHeaderLabels(["Course"])

        courses_root = self.course_selector_model.invisibleRootItem()

        for term, courses in self.group_courses_by_term(self.courses):
            term_node = QStandardItem(term.name)

            for course in courses:
                term_node.appendRow(ContainerItem(course))
                self.resources.update({resource.id: resource for resource in course.resources})

            courses_root.appendRow(term_node)

        self.course_selector.expandAll()
        # self.link_transformer.files = self.resources

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
        await self.data_manager.update_course_preferences(self.selected_course.preferences)
        self.file_viewer.load_course_files(self.selected_course)

