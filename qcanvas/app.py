import asyncio
import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

import qcanvas.backend_connectors.qcanvas_task_master as task_master
import qcanvas.settings as settings
from libqcanvas.qcanvas import QCanvas
from qcanvas.backend_connectors import FrontendResourceManager
from qcanvas.theme import app_theme
from qcanvas.ui.qcanvas_window import QCanvasWindow
from qcanvas.ui.setup import SetupDialog, setup_checker
from qcanvas.util import paths, runtime

_logger = logging.getLogger(__name__)
app = QApplication(sys.argv)


async def setup_database() -> QCanvas[FrontendResourceManager]:
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
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set, Qt.ConnectionType.SingleShotConnection)

    async def coro():
        setup_window = SetupDialog()
        setup_window.rejected.connect(lambda: exit())
        setup_window.show()
        await app_close_event.wait()

    asyncio.run(coro(), loop_factory=QEventLoop)


def launch():
    if runtime.is_running_as_flatpak:
        QGuiApplication.setDesktopFileName("io.github.qcanvas.QCanvasApp")

    app.setApplicationName("QCanvas")

    task_master.register()
    app_theme.theme = settings.ui.theme

    if setup_checker.needs_setup():
        run_setup()

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set, Qt.ConnectionType.SingleShotConnection)

    async def async_main():
        _qcanvas = await setup_database()

        _main_window = QCanvasWindow(_qcanvas)
        _main_window.show()
        await app_close_event.wait()

    asyncio.run(async_main(), loop_factory=QEventLoop)
