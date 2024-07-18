import logging

from rich.console import Console
from rich.logging import RichHandler

_console = Console(file=open("debug.log", "w"))

logging.basicConfig(
    level="WARN",
    handlers=[
        RichHandler(),
        RichHandler(rich_tracebacks=False, console=_console),
    ],
    format="%(message)s",
    datefmt="[%X]",
)
logging.getLogger("qcanvas").setLevel(logging.DEBUG)
logging.getLogger("qcanvas_backend").setLevel(logging.DEBUG)
# logging.getLogger("qcanvas_api_clients").setLevel(logging.DEBUG)
_logger = logging.getLogger(__name__)

import asyncio
import sys

from qasync import QEventLoop
from qtpy.QtWidgets import QApplication

from qcanvas.ui.main_ui.qcanvas_window import QCanvasWindow
from qcanvas.ui.setup import SetupDialog, setup_checker

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
