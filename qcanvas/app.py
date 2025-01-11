import asyncio
import logging
import sys

from libqcanvas.qcanvas import QCanvas
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop, asyncSlot

import qcanvas.backend_connectors.qcanvas_task_master as task_master
from qcanvas.backend_connectors import FrontendResourceManager
from qcanvas.ui.qcanvas_window import QCanvasWindow
from qcanvas.ui.setup import SetupDialog, setup_checker
from qcanvas.util import paths, runtime
from qcanvas.theme import app_theme
import qcanvas.settings as settings

_logger = logging.getLogger(__name__)
app = QApplication(sys.argv)


# I couldn't figure out a reliable way of getting the event loop started.
# This just uses a signal with an async slot to run some async functions and then shows the main window
class _MainStarter(QObject):
    _starting = Signal()

    def __init__(self):
        super().__init__()
        self._starting.connect(self._start, Qt.ConnectionType.SingleShotConnection)

    def start(self):
        self._starting.emit()

    @asyncSlot()
    async def _start(self):
        _qcanvas = await self._setup_database()

        _main_window = QCanvasWindow(_qcanvas)
        _main_window.show()
        self.setParent(_main_window)

    async def _setup_database(self) -> QCanvas[FrontendResourceManager]:
        _qcanvas = QCanvas[FrontendResourceManager](
            canvas_config=settings.client.canvas_config,
            panopto_config=settings.client.panopto_config,
            storage_path=paths.data_storage(),
            resource_manager_class=FrontendResourceManager,
        )

        await _qcanvas.database.upgrade()
        await _qcanvas.init()

        return _qcanvas


def run_setup():
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set, Qt.ConnectionType.SingleShotConnection)

    setup_window = SetupDialog()
    setup_window.show()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())


def launch():
    if runtime.is_running_as_flatpak:
        QGuiApplication.setDesktopFileName("io.github.qcanvas.QCanvasApp")

    app.setApplicationName("QCanvas")

    task_master.register()
    app_theme.theme = settings.ui.theme

    if setup_checker.needs_setup():
        run_setup()

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set, Qt.ConnectionType.SingleShotConnection)

    _main = _MainStarter()
    _main.start()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
