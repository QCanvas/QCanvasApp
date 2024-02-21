import asyncio
import logging
import sys
from datetime import datetime

import httpx
import qdarktheme
from httpx import URL
from qasync import QEventLoop, asyncSlot
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker

import qcanvas.db as db
from qcanvas.QtVersionHelper.QtCore import Signal
from qcanvas.QtVersionHelper.QtWidgets import QApplication, QProgressDialog, QMainWindow
from qcanvas.net.canvas.canvas_client import CanvasClient
from qcanvas.ui.main_ui import AppMainWindow
from qcanvas.ui.setup_dialog import SetupDialog
from qcanvas.util import AppSettings
from qcanvas.util.constants import app_name
from qcanvas.util.course_indexer import DataManager
from qcanvas.util.linkscanner import CanvasFileScanner
from qcanvas.util.linkscanner.canvas_media_object_scanner import CanvasMediaObjectScanner
from qcanvas.util.linkscanner.dropbox_scanner import DropboxScanner

engine = create_async_engine("sqlite+aiosqlite:///meme", echo=False)

logging.basicConfig()
logging.getLogger("canvas_client").setLevel(logging.DEBUG)

async def begin():
    # Create meta stuff
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)


class LoaderWindow(QMainWindow):
    init = Signal()
    setup = Signal()
    ready = Signal()

    def __init__(self):
        super().__init__()
        self.init.connect(self.on_init)
        self.setup.connect(self.on_setup)
        self.ready.connect(self.on_ready)
        self.setWindowTitle(app_name)
        self.setCentralWidget(QProgressDialog("Verifying config", None, 0, 0))

        self.init.emit()


    @asyncSlot()
    async def on_init(self):
        try:
            if not await CanvasClient.verify_config(AppSettings.canvas_url, AppSettings.canvas_api_key):
                self.setup.emit()
            else:
                self.ready.emit()
        except:
            self.setup.emit()

    @asyncSlot()
    async def on_setup(self):
        setup = SetupDialog(self)
        setup.rejected.connect(lambda: sys.exit(0))
        setup.accepted.connect(self.on_ready)
        setup.show()

    @asyncSlot()
    async def on_ready(self):
        client = CanvasClient(canvas_url=URL(AppSettings.canvas_url), api_key=AppSettings.canvas_api_key)
        data_manager = DataManager(
            client=client,
            link_scanners=[CanvasFileScanner(client), DropboxScanner(httpx.AsyncClient()),
                           CanvasMediaObjectScanner(client.client)],
            sessionmaker=AsyncSessionMaker(engine, expire_on_commit=False),
            last_update=datetime.min
        )

        await data_manager.init()
        self.close()
        self.open_main_app(data_manager)

    def open_main_app(self, data_manager: DataManager):
        self.main_window = AppMainWindow(data_manager)
        self.main_window.setWindowTitle(app_name)
        self.main_window.show()
        # Set the main window as the parent of this window so this window is destroyed when the main window is closed
        self.setParent(self.main_window)


if __name__ == '__main__':
    asyncio.run(begin())

    app = QApplication(sys.argv)
    c = app.palette().base().color()
    print(f"{c.red()} {c.green()} {c.blue()}")
    qdarktheme.setup_theme("light",
                           custom_colors={"primary": "FF804F"}
    )

    event_loop = QEventLoop()
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    loader_window = LoaderWindow()
    loader_window.show()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())

    print("Exiting")
