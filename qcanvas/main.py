import asyncio
import json
import logging
import sys
from datetime import datetime
from typing import Sequence

from PySide6.QtWidgets import QApplication
from httpx import URL
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker, AsyncSession
from sqlalchemy.orm import selectinload

from qcanvas.ui.main_ui import AppMainWindow
from qcanvas.util.linkscanner import CanvasFileScanner
from qcanvas.util.course_loader import CourseLoader
from qcanvas.net.canvas.canvas_client import CanvasClient
from qcanvas import queries
from qcanvas.util import AppSettings

import qcanvas.db as db
from QtVersionHelper import run_app


client = CanvasClient(canvas_url=URL(AppSettings.canvas_url()), api_key=AppSettings.canvas_api_key())

engine = create_async_engine("sqlite+aiosqlite:///meme", echo=False)

logging.basicConfig()
logging.getLogger("module_item_loader").setLevel(logging.DEBUG)
# logging.getLogger("aiosqlite").setLevel(logging.DEBUG)

loader = CourseLoader(
    client=client,
    link_scanners=[CanvasFileScanner(client)], #DropboxScanner(client.client)],
    sessionmaker=AsyncSessionMaker(engine, expire_on_commit=False),
    last_update=datetime.min
)

async def run():
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    start = datetime.now()
    # query = (await client.do_graphql_query(gql(queries.all_courses.DEFINITION), detailed=True))
    # print(json.dumps(query))
    _json = json.load(open("../run/all_courses_data.json"))
    result = queries.AllCoursesQueryData(**_json)

    await loader.load_courses_data(result.all_courses)
    # await loader.update_db()

    end = datetime.now()
    print(end - start)


async def get_course_data() -> Sequence[db.Course]:
    async with AsyncSession(engine, expire_on_commit=False) as session, session.begin():
        return (await session.execute(select(db.Course)
                                      .options(
            selectinload(db.Course.modules)
            .joinedload(db.Module.course),
            selectinload(db.Course.modules)
            .joinedload(db.Module.items)
            .selectin_polymorphic([db.ModulePage, db.ModuleFile])
            .joinedload(db.ModuleItem.module),
            selectinload(db.Course.assignments)
            .joinedload(db.Assignment.course),
            selectinload(db.Course.assignments)
            .joinedload(db.Assignment.resources)
            # .joinedload(db.ModuleItem.module)
            # .joinedload(db.ModuleItem.)
        ))).scalars().all()


if __name__ == '__main__':
    asyncio.run(run())

    app = QApplication()

    widget = AppMainWindow(asyncio.run(get_course_data()))
    widget.resize(800, 600)
    widget.show()

    sys.exit(run_app(app))




