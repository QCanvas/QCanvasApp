import logging
from asyncio import Event
from datetime import datetime
from typing import Sequence, Union, Optional

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from qasync import asyncSlot

from qcanvas.QtVersionHelper.QtGui import QStandardItemModel, QStandardItem
from qcanvas.QtVersionHelper.QtWidgets import *
from qcanvas.QtVersionHelper.QtCore import QItemSelection, Slot, Signal, Qt, QObject, QModelIndex

import qcanvas.db.database as db
from qcanvas.ui.container_item import ContainerItem
from qcanvas.ui.viewer.course_list import CourseList
from qcanvas.ui.viewer.file_list import FileRow
from qcanvas.ui.viewer.file_view_tab import FileViewTab
from qcanvas.ui.viewer.page_list_viewer import AssignmentsViewer, PagesViewer, LinkTransformer
from qcanvas.util import AppSettings
from qcanvas.util.constants import app_name
from qcanvas.util.course_indexer import DataManager

_aux_settings = AppSettings.auxiliary

class AppMainWindow(QMainWindow):
    logger = logging.getLogger()
    loaded = Signal()
    operation_lock = Event()

    def __init__(self, data_manager: DataManager, parent: QWidget | None = None):
        super().__init__(parent)

        self.selected_course: db.Course | None = None
        self.courses: Sequence[db.Course] = []
        self.resources: dict[str, db.Resource] = {}
        self.data_manager = data_manager
        self.link_transformer = LinkTransformer(self.data_manager.link_scanners, self.resources)

        right_splitter = QSplitter()
        right_splitter.setOrientation(Qt.Orientation.Vertical)

        self.sync_button = QPushButton("Synchronize")
        self.sync_button.clicked.connect(self.sync_data)

        self.course_list = CourseList(self.data_manager)
        self.course_list.course_selected.connect(self.on_course_selected)

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
        h_layout.addWidget(self.course_list)
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

        self.read_settings()

    def closeEvent(self, event):
        _aux_settings.setValue("geometry", self.saveGeometry())
        _aux_settings.setValue("windowState", self.saveState())

    def read_settings(self):
        self.restoreGeometry(_aux_settings.value("geometry"))
        self.restoreState(_aux_settings.value("windowState"))

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



    @asyncSlot()
    async def load_course_list(self):
        self.courses = (await self.data_manager.get_data())
        self.selected_course = None
        self.resources.clear()

        for course in self.courses:
            self.resources.update({resource.id: resource for resource in course.resources})

        self.course_list.load_course_list(self.courses)


    @Slot(db.Course)
    def on_course_selected(self, course: Optional[db.Course]):
        if course is not None:
            self.selected_course = course
            self.pages_viewer.fill_tree(course)
            self.assignment_viewer.fill_tree(course)
            self.file_viewer.load_course_files(course)
        else:
            self.selected_course = None
            self.file_viewer.clear()


    @asyncSlot(db.CoursePreferences)
    async def course_file_group_by_preference_changed(self, preference: db.GroupByPreference):
        self.selected_course.preferences.files_group_by_preference = preference
        await self.data_manager.update_item(self.selected_course.preferences)
        self.file_viewer.load_course_files(self.selected_course)

