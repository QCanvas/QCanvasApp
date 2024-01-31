import asyncio
import json
from datetime import datetime

from gql import gql
from httpx import URL
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import undefer, load_only, selectin_polymorphic, selectinload

from qcanvas.util import link_scanner
from qcanvas.util.module_item_loader import ModuleItemLoader
from qcanvas.net.canvas.canvas_client import CanvasClient
from qcanvas import queries
from qcanvas.util import AppSettings

import qcanvas.db as db

client = CanvasClient(canvas_url=URL(AppSettings.canvas_url()), api_key=AppSettings.canvas_api_key())

engine = create_async_engine("sqlite+aiosqlite:///test", echo=False)


async def load_all_pages(result: queries.AllCoursesQueryData):
    loader: ModuleItemLoader

    async with AsyncSession(engine, expire_on_commit=False) as session, session.begin():
        loader = ModuleItemLoader(
            existing_module_items=(await session.execute(select(db.ModuleItem).options(selectinload(db.ModuleItem.resources), selectin_polymorphic(db.ModuleItem, [db.ModulePage, db.ModuleFile])))).scalars().all(),
            existing_resources=(await session.execute(select(db.Resource))).scalars().all(),
            client=client,
            link_scanners=[link_scanner.CanvasLinkedResourceHandler(client)]
        )

    tasks = []

    for g_course in result.all_courses:
        for g_module in g_course.modules_connection.nodes:
            for g_module_item in g_module.module_items:
                content = g_module_item.content
                if isinstance(content, queries.File):
                    tasks.append(asyncio.create_task(loader.load_module_file(content, g_course, g_module)))
                elif isinstance(content, queries.Page):
                    tasks.append(asyncio.create_task(loader.load_module_page(content, g_course, g_module)))

    await asyncio.wait(tasks)

    await loader.scan_pages_for_file_links()

    await loader.update_db(engine)


# async def scan_all_pages_for_files():
#     async with AsyncSession(engine) as session, session.begin():
#         pages = (await session.execute(select(db.ModulePage))).scalars().all()
#
#         for page in pages:
#             soup = BeautifulSoup(page.content, 'html.parser')
#
#             for link in soup.find_all('a'):
#                 if "data-api-returntype" in link.attrs.keys() and link["data-api-returntype"] == "File":
#                     # print(link["data-api-endpoint"])
#                     id = URL(link["data-api-endpoint"]).path.rsplit('/', 2)[-1]
#
                    # print((await session.get_one(db.Resource, id)).file_name)


async def run():
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    start = datetime.now()
    query = (await client.do_graphql_query(gql(queries.all_courses.DEFINITION), detailed=True))
    # print(json.dumps(query))
    # _json = json.load(open("../run/all_courses_data.json"))
    result = queries.AllCoursesQueryData(**query)


    # await scan_all_pages_for_files()

    async with AsyncSession(engine) as session, session.begin():
        for g_course in result.all_courses:
            await session.merge(db.convert_term(g_course.term))
            course = await session.merge(db.convert_course(g_course))
            course.term_id = g_course.term.q_id

            for g_module in g_course.modules_connection.nodes:
                module = db.convert_module(g_module)
                module.course_id = course.id
                await session.merge(module)

            for g_assignment in g_course.assignments_connection.nodes:
                assignment = db.convert_assignment(g_assignment)
                assignment.course_id = g_course.m_id
                await session.merge(assignment)

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
