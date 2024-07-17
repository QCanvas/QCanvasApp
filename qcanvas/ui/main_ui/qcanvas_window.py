import logging
from threading import Semaphore
from typing import *

import qcanvas_backend.database.types as db
# from block_timer.timer import Timer
from qasync import asyncSlot
from qcanvas_backend.database.data_monolith import DataMonolith
from qcanvas_backend.qcanvas import QCanvas
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import *

from qcanvas import icons
from qcanvas.ui.course_viewer.course_viewer import CourseViewer
from qcanvas.ui.main_ui.course_tree import CourseTree
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
        self._course_viewer: Optional[CourseViewer] = None
        self._course_stack = QStackedWidget()
        self._viewers: dict[str, CourseViewer] = {}

        # fixme terrible
        h_box = QHBoxLayout()
        v_box = QVBoxLayout()
        v_box.addWidget(self._course_tree)
        v_box.addWidget(self._sync_button)
        h_box.addLayout(v_box)
        h_box.addWidget(self._course_stack)
        h_box.setStretch(0, 1)
        h_box.setStretch(1, 5)

        w = QWidget()
        w.setLayout(h_box)
        self.setCentralWidget(w)

        self._loaded.connect(self._load_db)
        self._loaded.emit()

    @asyncSlot()
    async def _load_db(self):
        await self._qcanvas.init()
        self._data = await self._qcanvas.get_data()
        await self._course_tree.load()

    @asyncSlot()
    async def _synchronise(self) -> None:
        if not self._operation_semaphore.acquire(False):
            _logger.debug("Sync operation already in progress")
            return

        try:
            await self._qcanvas.synchronise_canvas()
            self._sync_button.setText("Done")
        finally:
            self._operation_semaphore.release()

    @Slot()
    def _course_selected(self, course: Optional[db.Course]):
        if course is not None:
            # fixme bad
            if course.id not in self._viewers:
                # with Timer():
                self._viewers[course.id] = CourseViewer(course)
                self._course_stack.addWidget(self._viewers[course.id])

            self._course_stack.setCurrentWidget(self._viewers[course.id])
