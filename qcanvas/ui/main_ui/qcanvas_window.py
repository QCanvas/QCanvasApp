import logging
from threading import Semaphore
from typing import *

import qcanvas_backend.database.types as db
from qasync import asyncSlot
from qcanvas_backend.database.data_monolith import DataMonolith
from qcanvas_backend.qcanvas import QCanvas
from qtpy.QtCore import QUrl
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import QDesktopServices, QKeySequence
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import *

from qcanvas import icons
from qcanvas.backend_connectors import FrontendResourceManager
from qcanvas.ui.course_viewer import CourseTree
from qcanvas.ui.main_ui.course_viewer_container import CourseViewerContainer
from qcanvas.ui.main_ui.status_bar_progress_display import StatusBarProgressDisplay
from qcanvas.util import paths, settings
from qcanvas.util.ui_tools import create_qaction

_logger = logging.getLogger(__name__)


class QCanvasWindow(QMainWindow):
    _loaded = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QCanvas")
        self.setWindowIcon(QPixmap(icons.main_icon))

        self._operation_semaphore = Semaphore()
        self._data: Optional[DataMonolith] = None
        self._qcanvas = QCanvas[FrontendResourceManager](
            canvas_config=settings.client.canvas_config,
            panopto_config=settings.client.panopto_config,
            storage_path=paths.data_storage(),
            resource_manager_class=FrontendResourceManager,
        )

        self._course_tree = CourseTree()
        self._course_tree.item_selected.connect(self._on_course_selected)
        self._course_tree.course_renamed.connect(self._on_course_renamed)
        self._sync_button = QPushButton("Synchronise")
        self._sync_button.clicked.connect(self._synchronise)
        self._course_viewer_container = CourseViewerContainer(
            self._qcanvas.resource_manager
        )

        self.setCentralWidget(self._setup_main_layout())
        self.setStatusBar(StatusBarProgressDisplay())
        self._setup_menu_bar()

        self._loaded.connect(self._load_db)
        self._loaded.emit()

    def _setup_menu_bar(self) -> None:
        menu_item = self.menuBar().addMenu("File")

        create_qaction(
            name="Open downloads folder",
            shortcut=QKeySequence("Ctrl+D"),
            triggered=self._open_downloads_folder,
            parent=menu_item,
        )

        create_qaction(
            name="Quick canvas login",
            shortcut=QKeySequence("Ctrl+O"),
            triggered=self._open_quick_auth_in_browser,
            parent=menu_item,
        )

        create_qaction(
            name="Quit",
            shortcut=QKeySequence("Ctrl+Q"),
            triggered=lambda: self.close(),
            parent=menu_item,
        )

    def _setup_main_layout(self) -> QWidget:
        h_box = QHBoxLayout()

        h_box.addLayout(self._setup_course_column(), 1)
        h_box.addWidget(self._course_viewer_container, 5)

        widget = QWidget()
        widget.setLayout(h_box)
        return widget

    def _setup_course_column(self) -> QVBoxLayout:
        course_list_column = QVBoxLayout()
        course_list_column.addWidget(self._course_tree)
        course_list_column.addWidget(self._sync_button)

        return course_list_column

    @asyncSlot()
    async def _load_db(self) -> None:
        await self._qcanvas.init()
        self._course_tree.reload(await self._get_terms(), sync_receipt=None)

    @asyncSlot()
    async def _synchronise(self) -> None:
        if not self._operation_semaphore.acquire(False):
            _logger.debug("Sync operation already in progress")
            return

        try:
            # todo handle exceptions and PROGRESS!! better
            self._sync_button.setText("Sync in progress...")
            receipt = await self._qcanvas.synchronise_canvas()

            self._course_tree.reload(await self._get_terms(), sync_receipt=receipt)
            await self._course_viewer_container.reload_all(
                await self._get_courses(), sync_receipt=receipt
            )
            self._sync_button.setText("Synchronise")

        finally:
            self._operation_semaphore.release()

    async def _get_terms(self) -> Sequence[db.Term]:
        return (await self._qcanvas.get_data()).terms

    async def _get_courses(self) -> Sequence[db.Course]:
        return (await self._qcanvas.get_data()).courses

    @Slot()
    def _on_course_selected(self, course: Optional[db.Course]) -> None:
        if course is not None:
            self._course_viewer_container.load_course(course)
        else:
            self._course_viewer_container.show_blank()

    @asyncSlot()
    async def _on_course_renamed(self, course: db.Course, new_name: str) -> None:
        _logger.debug("Rename %s -> %s", course.name, new_name)

        async with self._qcanvas.database.session() as session:
            session.add(course)
            course.configuration.nickname = new_name

    @asyncSlot()
    async def _open_quick_auth_in_browser(self):
        opening_progress_dialog = QProgressDialog("Opening canvas", None, 0, 0, self)
        opening_progress_dialog.setWindowTitle("Please wait")
        opening_progress_dialog.show()
        QDesktopServices.openUrl(
            await self._qcanvas.canvas_client.get_temporary_session_url()
        )
        opening_progress_dialog.close()

    @Slot()
    def _open_downloads_folder(self) -> None:
        # fixme hard coded path! >:(
        QDesktopServices.openUrl(
            QUrl(f"file://{(paths.data_storage() / 'downloads').absolute()}")
        )
