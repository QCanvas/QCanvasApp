import asyncio
import logging
import sys

from qasync import QEventLoop
from qtpy.QtWidgets import QApplication

from qcanvas.ui.main_ui.qcanvas_window import QCanvasWindow
from qcanvas.ui.setup import SetupDialog, setup_checker

_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    if setup_checker.needs_setup():
        w = SetupDialog()
        w.show()

    m = QCanvasWindow()
    m.show()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
