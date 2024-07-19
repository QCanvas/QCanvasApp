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
logging.getLogger("qcanvas_backend").setLevel(logging.INFO)
logging.getLogger("qcanvas.ui.memory_tree").setLevel(logging.INFO)
# logging.getLogger("qcanvas_api_clients").setLevel(logging.DEBUG)
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

    # qdarktheme.setup_theme(
    #     "light",
    #     custom_colors={
    #         "primary": "e21d31",
    #         "[light]": {"foreground": "480910", "background": "fcf8f8"},
    #         "[dark]": {"foreground": "fbdfe2", "background": "231f1f"},
    #     },
    # )

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
