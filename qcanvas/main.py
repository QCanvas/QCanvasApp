import asyncio
import json
import logging
from datetime import datetime

from httpx import URL
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import undefer, load_only, selectin_polymorphic, selectinload
from sqlalchemy.ext.asyncio.session import async_sessionmaker as AsyncSessionMaker

from qcanvas.util import link_scanner
from qcanvas.util.module_item_loader import ModuleItemLoader
from qcanvas.net.canvas.canvas_client import CanvasClient
from qcanvas import queries
from qcanvas.util import AppSettings

import qcanvas.db as db

client = CanvasClient(canvas_url=URL(AppSettings.canvas_url()), api_key=AppSettings.canvas_api_key())

engine = create_async_engine("sqlite+aiosqlite:///test", echo=False)

logger = logging.getLogger()
logging.getLogger("module_item_loader").setLevel(logging.DEBUG)

async def load_all_pages(result: queries.AllCoursesQueryData):
    loader: ModuleItemLoader

    async with AsyncSession(engine, expire_on_commit=False) as session, session.begin():
        loader = ModuleItemLoader(
            client=client,
            link_scanners=[link_scanner.CanvasLinkedResourceHandler(client)],
            sessionmaker=AsyncSessionMaker(engine, expire_on_commit=False)
        )


    await loader.load_data_from_query(result)
    # await loader.scan_pages_for_file_links()


async def run():
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    start = datetime.now()
    # query = (await client.do_graphql_query(gql(queries.all_courses.DEFINITION), detailed=True))
    # print(json.dumps(query))
    _json = json.load(open("../run/all_courses_data.json"))
    result = queries.AllCoursesQueryData(**_json)


    async with AsyncSession(engine) as session, session.begin():


        await session.flush()
        """
        select module_items.id, module_items.name, module_items.type
        from (select modules.id from modules where modules.course_id = 'Q291cnNlLTIxOTc0') as course_modules
        join module_items
        on module_items.module_id = course_modules.id
        """
        # sub = select(db.Module.id).where(db.Module.course_id == "Q291cnNlLTIxOTc0").subquery()
        #
        # for fart in (await session.execute(select(db.ModuleItem).join(sub))).scalars().all():
        #     print(fart.id, fart.name)

    await load_all_pages(result)

    end = datetime.now()

    print(end - start)

asyncio.run(run())
