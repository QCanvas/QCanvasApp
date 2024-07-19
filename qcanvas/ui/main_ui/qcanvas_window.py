import logging
from threading import Semaphore
from typing import *

import qcanvas_backend.database.types as db
from qasync import asyncSlot
from qcanvas_backend.database.data_monolith import DataMonolith
from qcanvas_backend.qcanvas import QCanvas
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import *

from qcanvas import icons
from qcanvas.ui.main_ui.course_tree import CourseTree
from qcanvas.ui.main_ui.course_viewer_container import CourseViewerContainer
from qcanvas.util import paths, settings
from qcanvas.util.fe_resource_manager import _RM

_logger = logging.getLogger(__name__)


class QCanvasWindow(QMainWindow):
    _loaded = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QCanvas")
        self.setWindowIcon(QPixmap(icons.main_icon))

        self._operation_semaphore = Semaphore()
        self._data: Optional[DataMonolith] = None
        self._qcanvas = QCanvas[_RM](
            canvas_config=settings.client.canvas_config,
            panopto_config=settings.client.panopto_config,
            storage_path=paths.data_storage(),
            resource_manager_class=_RM,
        )
        self._course_tree = CourseTree(self._qcanvas)
        self._course_tree.course_selected.connect(self._course_selected)
        self._sync_button = QPushButton("Synchronise")
        self._sync_button.clicked.connect(self._synchronise)
        self._course_viewer_container = CourseViewerContainer(self._qcanvas)

        self.setCentralWidget(self._setup_main_layout())
        self._loaded.connect(self._load_db)
        self._loaded.emit()

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
        await self._course_tree.load(await self._get_terms(), sync_receipt=None)

    @asyncSlot()
    async def _synchronise(self) -> None:
        if not self._operation_semaphore.acquire(False):
            _logger.debug("Sync operation already in progress")
            return

        try:
            receipt = await self._qcanvas.synchronise_canvas()

            await self._course_tree.reload(
                await self._get_terms(), sync_receipt=receipt
            )
            await self._course_viewer_container.reload_all(
                await self._get_courses(), sync_receipt=receipt
            )

            self._sync_button.setText("Done")

        finally:
            self._operation_semaphore.release()

    async def _get_terms(self) -> Sequence[db.Term]:
        return (await self._qcanvas.get_data()).terms

    async def _get_courses(self) -> Sequence[db.Course]:
        return (await self._qcanvas.get_data()).courses

    @Slot()
    def _course_selected(self, course: Optional[db.Course]):
        if course is not None:
            self._course_viewer_container.load_course(course)
        else:
            self._course_viewer_container.show_blank()
