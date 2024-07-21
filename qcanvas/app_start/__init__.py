import asyncio
import sys

import qdarktheme
from qasync import QEventLoop
from qtpy.QtWidgets import QApplication

import qcanvas.backend_connectors.qcanvas_task_master as task_master
from qcanvas.ui.main_ui.qcanvas_window import QCanvasWindow
from qcanvas.ui.setup import SetupDialog, setup_checker

main_window = None
setup_window = None


def _show_main():
    global main_window
    main_window = QCanvasWindow()
    main_window.show()


def launch():
    app = QApplication(sys.argv)
    app.setApplicationName("QCanvas")

    task_master.register()

    qdarktheme.setup_theme(
        "auto",
        custom_colors={"primary": "e02424"},
    )

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    if setup_checker.needs_setup():
        setup_window = SetupDialog()
        setup_window.show()
        setup_window.closed.connect(_show_main)
    else:
        _show_main()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
