import asyncio
import logging
import sys
from datetime import datetime

import httpx
from qcanvas.QtVersionHelper.QtWidgets import QApplication
from httpx import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker

from qcanvas.ui.main_ui import AppMainWindow
from qcanvas.util.linkscanner import CanvasFileScanner
from qcanvas.util.course_indexer import DataManager
from qcanvas.net.canvas.canvas_client import CanvasClient
from qcanvas.util import AppSettings

from qcanvas.util.linkscanner.canvas_media_object_scanner import CanvasMediaObjectScanner
from qcanvas.util.linkscanner.dropbox_scanner import DropboxScanner

from qasync import QEventLoop
import qcanvas.db as db
import qdarktheme

client = CanvasClient(canvas_url=URL(AppSettings.canvas_url), api_key=AppSettings.canvas_api_key)

engine = create_async_engine("sqlite+aiosqlite:///meme", echo=False)

logging.basicConfig()
logging.getLogger("canvas_client").setLevel(logging.DEBUG)
# logging.getLogger("aiosqlite").setLevel(logging.DEBUG)

data_manager = DataManager(
    client=client,
    link_scanners=[CanvasFileScanner(client), DropboxScanner(httpx.AsyncClient()),
                   CanvasMediaObjectScanner(client.client)],
    sessionmaker=AsyncSessionMaker(engine, expire_on_commit=False),
    last_update=datetime.min
)

data_manager.download_pool.download_progress_updated.connect(lambda x, y: print(f"Progress {x} {y}"))

async def begin():
    # Create meta stuff
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    await data_manager.init()


if __name__ == '__main__':
    asyncio.run(begin())

    app = QApplication(sys.argv)

    qdarktheme.setup_theme("light")

    event_loop = QEventLoop()
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    main_window = AppMainWindow(data_manager)
    main_window.resize(800, 600)
    main_window.show()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())

    print("Exiting")
