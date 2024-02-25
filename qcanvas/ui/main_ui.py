import logging
import sys
import traceback
from typing import Sequence, Optional

from PySide6.QtCore import Slot, Signal, Qt, QUrl, QObject
from PySide6.QtGui import QDesktopServices, QKeySequence
from PySide6.QtWidgets import *
from qasync import asyncSlot

import qcanvas.db.database as db
from qcanvas.ui.menu_bar.grouping_preferences_menu import GroupingPreferencesMenu
from qcanvas.ui.menu_bar.theme_selection_menu import ThemeSelectionMenu
from qcanvas.ui.status_bar_reporter import StatusBarReporter
from qcanvas.ui.viewer.course_list import CourseList
from qcanvas.ui.viewer.file_list import FileRow
from qcanvas.ui.viewer.file_view_tab import FileViewTab
from qcanvas.ui.viewer.page_list_viewer import AssignmentsViewer, PagesViewer, LinkTransformer
from qcanvas.util import self_updater
from qcanvas.util.app_settings import settings
from qcanvas.util.constants import app_name
from qcanvas.util.course_indexer import DataManager
from qcanvas.util.helpers.qaction_helper import create_qaction

_aux_settings = settings.auxiliary
_no_course_selected_text = "No course selected"

class AppMainWindow(QMainWindow):
    logger = logging.getLogger()
    loaded = Signal()
    files_grouping_preference_changed = Signal(db.GroupByPreference)

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
        self.file_viewer.files_column.tree.itemActivated.connect(self.download_file_from_file_pane)
        self.file_viewer.assignment_files_column.tree.itemActivated.connect(self.download_file_from_file_pane)

        self.tab_widget = QTabWidget()
        self.tab_widget.insertTab(0, self.file_viewer, "Files")
        self.tab_widget.insertTab(1, self.assignment_viewer, "Assignments")
        self.tab_widget.insertTab(2, self.pages_viewer, "Pages")

        self.course_name_label = QLabel(_no_course_selected_text)
        self.course_name_label.setStyleSheet("font-weight: bold;")
        course_stack_layout = self.create_layout_and_add_widgets(QVBoxLayout, self.course_name_label, self.tab_widget)

        h_layout = self.create_layout_and_add_widgets(QHBoxLayout, self.course_list, course_stack_layout)
        h_layout.setStretch(1, 1)

        widget = QWidget()
        widget.setLayout(self.create_layout_and_add_widgets(QVBoxLayout, h_layout, self.sync_button))
        self.setCentralWidget(widget)

        self.setup_menu_bar()

        self.files_grouping_preference_changed.connect(self.on_grouping_preference_changed)

        self.loaded.connect(self.load_course_list)
        self.loaded.connect(self.check_for_update)
        self.loaded.emit()

        self.restore_window_position()

        # Activate the statusbar so it doesn't just appear randomly later
        bar: QStatusBar = self.statusBar()
        # Set its height so it doesn't get bigger when there's a progress bar in it
        bar.setFixedHeight(bar.height())

    @staticmethod
    def create_layout_and_add_widgets(layout_type: type, *widgets) -> QLayout:
        layout = layout_type()

        for widget in widgets:
            if isinstance(widget, QLayout):
                layout.addLayout(widget)
            else:
                layout.addWidget(widget)

        return layout

    def setup_menu_bar(self):
        menu_bar = self.menuBar()

        app_menu: QMenu = menu_bar.addMenu("App")
        view_menu: QMenu = menu_bar.addMenu("View")

        app_menu.addAction(self.setup_quick_authentication_action(app_menu))
        app_menu.addMenu(ThemeSelectionMenu())
        view_menu.addMenu(self.setup_group_by_menu())

    def setup_group_by_menu(self) -> QMenu:
        file_grouping_menu = GroupingPreferencesMenu(self.data_manager)
        self.course_list.course_selected.connect(file_grouping_menu.course_changed)
        file_grouping_menu.preference_changed.connect(self.on_grouping_preference_changed)

        return file_grouping_menu

    def setup_quick_authentication_action(self, parent: QObject):
        return create_qaction(
            name="Quick canvas login",
            shortcut=QKeySequence("Ctrl+O"),
            triggered=self.open_quick_auth_in_browser,
            parent=parent
        )

    @asyncSlot()
    async def open_quick_auth_in_browser(self):
        opening_progress_dialog = QProgressDialog("Opening canvas", None, 0, 0, self)
        opening_progress_dialog.setWindowTitle("Please wait")
        opening_progress_dialog.show()
        QDesktopServices.openUrl(await self.data_manager.client.get_temp_session_link())
        opening_progress_dialog.close()

    def closeEvent(self, event):
        settings.geometry = self.saveGeometry()
        settings.window_state = self.saveState()

    def restore_window_position(self):
        self.restoreGeometry(settings.geometry)
        self.restoreState(settings.window_state)

    @asyncSlot(QUrl)
    async def viewer_link_clicked(self, url: QUrl):
        # The url of a transformed link will start with a specific prefix
        if url.toString().startswith(LinkTransformer.transformed_url_prefix):
            # The rest of the 'url' is just the file id
            resource = self.resources[url.toString().removeprefix(LinkTransformer.transformed_url_prefix)]

            await self.data_manager.download_resource(resource)
            QDesktopServices.openUrl(QUrl.fromLocalFile(resource.download_location.absolute()))
        else:
            QDesktopServices.openUrl(url)

    @asyncSlot(QTreeWidgetItem, int)
    async def download_file_from_file_pane(self, item: QTreeWidgetItem, _: int):
        if isinstance(item, FileRow):
            await self.data_manager.download_resource(item.resource)
            QDesktopServices.openUrl(QUrl.fromLocalFile(item.resource.download_location.absolute()))

    @asyncSlot()
    async def sync_data(self):
        self.sync_button.setEnabled(False)
        self.sync_button.setText("Synchronizing")
        try:
            await self.data_manager.synchronize_with_canvas(StatusBarReporter(self.statusBar()))
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

    @asyncSlot()
    async def check_for_update(self):
        try:
            newer_version, installed_version = await self_updater.get_newer_version()

            if newer_version is not None and newer_version != settings.ignored_update:
                msg_box = QMessageBox(
                    QMessageBox.Icon.Question,
                    "Update available",
                    f"There is an update available ({installed_version} -> {newer_version})\nDo you want to update?\nThe program will close after the update is finished.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    self
                )

                def ignore_update():
                    settings.ignored_update = newer_version

                msg_box.accepted.connect(self.do_self_update)
                msg_box.rejected.connect(ignore_update)
                msg_box.show()
            else:
                print("No update available (or skipping this update)")
        except BaseException as e:
            sys.stderr.write(f"Could not check for updates: {e}\n")
            traceback.print_exc()
            sys.stderr.write("This can be ignored if in a dev environment\n")

    @asyncSlot()
    async def do_self_update(self):
        try:
            progress_diag = QProgressDialog("Updating", None, 0, 0, self)
            progress_diag.setWindowTitle(app_name)
            progress_diag.show()
            await self_updater.do_update()
            self.close()
        except BaseException as e:
            traceback.print_exc()

            QMessageBox(
                QMessageBox.Icon.Critical,
                "Error",
                "An error occurred during the update",
                parent=self
            ).show()

    @Slot(db.Course)
    def on_course_selected(self, course: Optional[db.Course]):
        if course is not None:
            self.selected_course = course
            # todo these should really be slots connected to this signal...
            self.pages_viewer.fill_tree(course)
            self.assignment_viewer.fill_tree(course)
            self.file_viewer.load_course_files(course)
            self.course_name_label.setText(course.name)
        else:
            self.selected_course = None
            self.file_viewer.clear()
            self.pages_viewer.clear()
            self.assignment_viewer.clear()
            self.course_name_label.setText(_no_course_selected_text)

    @asyncSlot(db.CoursePreferences)
    async def on_grouping_preference_changed(self):
        self.file_viewer.load_course_files(self.selected_course)
