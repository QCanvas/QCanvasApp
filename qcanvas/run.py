import logging

import qdarktheme
from rich.console import Console
from rich.logging import RichHandler

from qcanvas.util import paths

paths.data_storage().mkdir(parents=True, exist_ok=True)
_console = Console(file=open(paths.data_storage() / "debug.log", "w"))

logging.basicConfig(
    level="INFO",
    handlers=[
        RichHandler(),
        RichHandler(rich_tracebacks=False, console=_console),
    ],
    format="%(message)s",
    datefmt="[%X]",
)

_logger = logging.getLogger(__name__)

import asyncio
import sys

from qasync import QEventLoop
from qtpy.QtWidgets import QApplication

from qcanvas.ui.main_ui.qcanvas_window import QCanvasWindow
from qcanvas.ui.setup import SetupDialog, setup_checker

main_window = None
setup_window = None


def show_main():
    global main_window
    main_window = QCanvasWindow()
    main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    qdarktheme.setup_theme(
        "light",
        custom_colors={"primary": "ff1814"},
    )

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    if setup_checker.needs_setup():
        setup_window = SetupDialog()
        setup_window.show()
        setup_window.closed.connect(show_main)
    else:
        show_main()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
