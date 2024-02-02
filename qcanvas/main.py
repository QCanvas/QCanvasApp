import asyncio
import json
import logging
from datetime import datetime

from httpx import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker

from qcanvas.util.linkscanner import CanvasLinkedResourceHandler
from qcanvas.util.course_loader import CourseLoader
from qcanvas.net.canvas.canvas_client import CanvasClient
from qcanvas import queries
from qcanvas.util import AppSettings

import qcanvas.db as db

client = CanvasClient(canvas_url=URL(AppSettings.canvas_url()), api_key=AppSettings.canvas_api_key())

engine = create_async_engine("sqlite+aiosqlite:///test", echo=False)

logging.basicConfig()
logging.getLogger("course_loader").setLevel(logging.DEBUG)

loader = CourseLoader(
    client=client,
    link_scanners=[CanvasLinkedResourceHandler(client)],
    sessionmaker=AsyncSessionMaker(engine, expire_on_commit=False)
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

    end = datetime.now()
    print(end - start)

if __name__ == '__main__':
    asyncio.run(run())
