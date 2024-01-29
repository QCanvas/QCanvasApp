import asyncio
import json
from typing import Any, Sequence

from gql import gql
from httpx import URL
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine

from net.canvas_client import CanvasClient
from qcanvas import queries
from util import AppSettings

import qcanvas.db.database as db
import qcanvas.db.db_converter_helper as db_conv

client = CanvasClient(canvas_url=URL(AppSettings.canvas_url()), api_key=AppSettings.canvas_api_key())

engine = create_async_engine("sqlite+aiosqlite://", echo=False)

class ModuleItemLoader:

    pull_sem = asyncio.Semaphore(100)

    module_items: dict[str, db.ModuleItem]
    resources: dict[str, db.Resource]

    def __init__(self, module_items: Sequence[db.ModuleItem], resources: Sequence[db.Resource]):
        self.module_items = dict((module_item.id, module_item) for module_item in module_items)
        self.resources = dict((resource.id, resource) for resource in resources)

    async def load_module_file(self, g_file: queries.File, g_course: queries.Course, g_module: queries.Module):
        if g_file.m_id in self.resources.keys() and g_file.m_id in self.module_items.keys():
            return

        if g_file.m_id in self.resources.keys():
            resource = self.resources[g_file.m_id]
        else:
            print(f"Loading file {g_file.display_name}")
            await asyncio.sleep(1)
            resource = db_conv.convert_file(g_file, 100)
            resource.course_id = g_course.q_id
            self.resources[resource.id] = resource

        if g_file.m_id in self.module_items.keys():
            page = self.module_items[g_file.m_id]
        else:
            page = db_conv.convert_file_page(g_file)
            page.module_id = g_module.q_id
            self.module_items[page.id] = page

        page.resources.append(resource)

    async def load_module_page(self, g_page: queries.Page, g_course: queries.Course, g_module: queries.Module):
        if g_page.m_id not in self.module_items.keys():

            async with self.pull_sem:
                #fixme this is shit
                try:
                    # print(f"Loading page {g_page.title}")

                    result = await client.get_page(g_page.m_id, g_course.m_id)
                    # print(result)
                    page = db_conv.convert_page(g_page, json.loads(result)["body"])
                    page.module_id = g_module.q_id
                    self.module_items[page.id] = page
                except:
                    print(result)
                    raise

    async def update_db(self, engine: AsyncEngine):
        async with AsyncSession(engine) as session, session.begin():
            session.add_all(self.module_items.values())
            session.add_all(self.resources.values())


async def run():
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    result = queries.all_courses.AllCoursesQueryData(**json.load(open("../run/all_courses_data.json")))

    loader: ModuleItemLoader

    async with AsyncSession(engine, expire_on_commit=False) as session, session.begin():
        loader = ModuleItemLoader((await session.execute(select(db.ModuleItem))).scalars(),
                                  (await session.execute(select(db.Resource))).scalars())

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

    await loader.update_db(engine)

    async with AsyncSession(engine) as session, session.begin():
        for g_course in result.all_courses:
            await session.merge(db_conv.convert_term(g_course.term))
            course = await session.merge(db_conv.convert_course(g_course))
            course.term_id = g_course.term.q_id

            for g_module in g_course.modules_connection.nodes:
                module = db_conv.convert_module(g_module)
                module.course_id = course.id
                await session.merge(module)

        # select module_items.id, module_items.name, module_items.type
        # from (select modules.id from modules where modules.course_id = 'Q291cnNlLTIxOTc0') as course_modules
        # join module_items
        # on module_items.module_id = course_modules.id
        sub = select(db.Module.id).where(db.Module.course_id == "Q291cnNlLTIxOTc0").subquery()

        for fart in (await session.execute(select(db.ModuleItem).join(sub))).scalars().all():
            print(fart.id, fart.name)


asyncio.run(run())
