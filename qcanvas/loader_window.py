import httpx
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QProgressDialog
from httpx import URL
from qasync import asyncSlot
from sqlalchemy.ext.asyncio import async_sessionmaker as AsyncSessionMaker

from qcanvas.__main__ import engine
from qcanvas.net.canvas import CanvasClient
from qcanvas.settings.app_settings import settings
from qcanvas.ui.main_ui import AppMainWindow
from qcanvas.ui.setup_dialog import SetupDialog
from qcanvas.util.constants import app_name
from qcanvas.util.course_indexer import DataManager
from qcanvas.util.link_scanner import CanvasFileScanner
from qcanvas.util.link_scanner.canvas_media_object_scanner import CanvasMediaObjectScanner
from qcanvas.util.link_scanner.dropbox_scanner import DropboxScanner


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
            if not all_set:
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
