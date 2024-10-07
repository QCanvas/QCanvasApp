import asyncio
import logging
import sys

import qtpy
from qasync import QEventLoop
from qcanvas_backend.qcanvas import QCanvas
from qtpy.QtGui import QGuiApplication
from qtpy.QtWidgets import QApplication

import qcanvas.backend_connectors.qcanvas_task_master as task_master
from qcanvas.backend_connectors import FrontendResourceManager
from qcanvas.ui.main_ui.qcanvas_window import QCanvasWindow
from qcanvas.ui.setup import SetupDialog, setup_checker
from qcanvas.util import paths, runtime, settings, themes

main_window = None
setup_window = None

_logger = logging.getLogger(__name__)


def _show_main():
    global main_window
    _qcanvas = asyncio.get_event_loop().run_until_complete(_setup_database())
    main_window = QCanvasWindow(_qcanvas)
    main_window.show()


async def _setup_database() -> QCanvas[FrontendResourceManager]:
    _qcanvas = QCanvas[FrontendResourceManager](
        canvas_config=settings.client.canvas_config,
        panopto_config=settings.client.panopto_config,
        storage_path=paths.data_storage(),
        resource_manager_class=FrontendResourceManager,
    )

    await _qcanvas.database.upgrade()
    await _qcanvas.init()

    return _qcanvas


def _show_qt_api_name():
    print(f"Using Qt bindings from {qtpy.API_NAME}")
    _logger.info("Using Qt bindings from %s", qtpy.API_NAME)


def launch():
    _show_qt_api_name()

    app = QApplication(sys.argv)

    if runtime.is_running_as_flatpak:
        QGuiApplication.setDesktopFileName("io.github.qcanvas.QCanvasApp")

    app.setApplicationName("QCanvas")

    task_master.register()
    themes.apply(settings.ui.theme)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    if setup_checker.needs_setup():
        setup_window = SetupDialog()
        setup_window.show()
        setup_window.closed.connect(_show_main)
    else:
        _show_main()

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
