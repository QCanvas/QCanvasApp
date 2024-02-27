import asyncio
import logging
import sys

import httpx
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QProgressDialog, QMainWindow
from httpx import URL
from qasync import QEventLoop, asyncSlot
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker

import qcanvas.db as db
# noinspection PyUnresolvedReferences
import qcanvas.icons
from qcanvas.net.canvas.canvas_client import CanvasClient
from qcanvas.ui.main_ui import AppMainWindow
from qcanvas.ui.setup_dialog import SetupDialog
from qcanvas.util import self_updater
from qcanvas.util.app_settings import settings
from qcanvas.util.constants import app_name, updated_and_needs_restart_return_code
from qcanvas.util.course_indexer import DataManager
from qcanvas.util.helpers import theme_helper
from qcanvas.util.link_scanner import CanvasFileScanner
from qcanvas.util.link_scanner.canvas_media_object_scanner import CanvasMediaObjectScanner
from qcanvas.util.link_scanner.dropbox_scanner import DropboxScanner

engine = create_async_engine("sqlite+aiosqlite:///canvas_db.😘", echo=False)

logging.basicConfig()
logging.getLogger("canvas_client").setLevel(logging.DEBUG)


class LoaderWindow(QMainWindow):
    """
    Responsible for verifying that the api key and canvas url is valid, then starting the main app.
    """
    init = Signal()
    setup = Signal()
    ready = Signal()

    def __init__(self):
        super().__init__()
        self.main_window: AppMainWindow | None = None
        self.main_icon = QPixmap(":/main_icon.svg")

        self.init.connect(self.on_init)
        self.setup.connect(self.on_setup)
        self.ready.connect(self.on_ready)

        self.setWindowTitle(app_name)
        self.setWindowIcon(self.main_icon)
        self.setCentralWidget(QProgressDialog("Verifying config", None, 0, 0))

        self.init.emit()

    @asyncSlot()
    async def on_init(self) -> None:
        try:
            all_set = None not in [settings.api_key, settings.canvas_url, settings.panopto_url]
            # Verify that the canvas urls and api key are valid
            if not all_set or not await CanvasClient.verify_config(settings.canvas_url, settings.api_key):
                # Show the setup dialog
                self.setup.emit()
            else:
                # Proceed to main app
                self.ready.emit()
        except:
            # If a problem occurred then something is probably invalid
            self.setup.emit()

    @asyncSlot()
    async def on_setup(self) -> None:
        """
        Shows the setup dialog
        """
        setup = SetupDialog(self, allow_cancel=False)
        setup.setWindowIcon(self.main_icon)
        setup.rejected.connect(lambda: self.close())
        setup.accepted.connect(self.on_ready)
        setup.show()

    @asyncSlot()
    async def on_ready(self) -> None:
        """
        Sets up the canvas client and data manager for the main app
        """
        client = CanvasClient(canvas_url=URL(settings.canvas_url), api_key=settings.api_key)
        data_manager = DataManager(
            client=client,
            link_scanners=[
                CanvasFileScanner(client),
                DropboxScanner(httpx.AsyncClient()),
                CanvasMediaObjectScanner(client.client)
            ],
            # Don't expire on commit because we need to take objects outside of the session
            sessionmaker=AsyncSessionMaker(engine, expire_on_commit=False)
        )

        await data_manager.init()
        self.close()
        self.open_main_app(data_manager)

    def open_main_app(self, data_manager: DataManager) -> None:
        """
        Starts the main app
        Parameters
        ----------
        data_manager
            The data manager the app will use
        """

        self.main_window = AppMainWindow(data_manager)
        self.main_window.setWindowTitle(app_name)
        self.main_window.setWindowIcon(self.main_icon)
        self.main_window.show()
        # Set the main window as the parent of this window so this window is destroyed when the main window is closed
        self.setParent(self.main_window)


async def setup_db():
    # Create meta stuff
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(setup_db())

    app = QApplication(sys.argv)

    # Apply the selected theme to qt
    theme_helper.apply_selected_theme()

    # Setup event loop for qasync
    event_loop = QEventLoop()
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    # Start the loader, which verifies the client config and initialises the data manager for the main program
    loader_window = LoaderWindow()
    loader_window.show()

    # For qasync
    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())

    print("Exiting")

    # Pass the 'restart needed' flag back to the launcher script, which will re-run the program.
    # See self_updater.do_update
    if self_updater.restart_flag:
        sys.exit(updated_and_needs_restart_return_code)
