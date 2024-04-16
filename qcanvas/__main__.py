import asyncio
import logging
import sys

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop
from sqlalchemy.ext.asyncio import create_async_engine

import qcanvas.db as db
# noinspection PyUnresolvedReferences
import qcanvas.icons
from qcanvas.loader_window import LoaderWindow
from qcanvas.util import self_updater
from qcanvas.util.constants import updated_and_needs_restart_return_code
from qcanvas.util.helpers import theme_helper

engine = create_async_engine("sqlite+aiosqlite:///canvas_db.😘", echo=False)

logging.basicConfig()
logging.getLogger("canvas_client").setLevel(logging.DEBUG)


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
