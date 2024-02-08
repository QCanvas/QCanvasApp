from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

import qcanvas.db as db
import qcanvas.queries as queries


async def create_assignments(g_course : queries.Course, session : AsyncSession) -> Sequence[db.Assignment]:
    assignments = []

    for g_assignment in g_course.assignments_connection.nodes:
        assignment = await session.get(db.Assignment, g_assignment.q_id)

        if assignment is None:
            assignment = db.Assignment()
            assignment.id = g_assignment.q_id
            assignment.course_id = g_course.m_id
            session.add(assignment)
        elif g_assignment.updated_at.replace(tzinfo=None) <= assignment.updated_at:
            continue

        assignment.name = g_assignment.name.strip("\t  ")
        assignment.description = g_assignment.description
        assignment.created_at = g_assignment.created_at
        assignment.updated_at = g_assignment.updated_at
        assignment.due_at = g_assignment.due_at
        assignment.position = g_assignment.position

        assignments.append(assignment)

    return assignments


async def create_modules(g_course : queries.Course, session: AsyncSession):
    for g_module in g_course.modules_connection.nodes:
        module = await session.get(db.Module, g_module.q_id)

        if module is None:
            module = db.Module()
            module.id = g_module.q_id
            module.course_id = g_course.m_id
            session.add(module)

        module.name = g_module.name


async def create_course(g_course : queries.Course, session: AsyncSession, term : db.Term):
    course = await session.get(db.Course, g_course.m_id)
    if course is None:
        course = db.Course()
        course.id = g_course.m_id
        session.add(course)
    course.name = g_course.name
    course.term = term


async def create_term(g_course : queries.Course, session) -> db.Term:
    term = await session.get(db.Term, g_course.term.q_id)

    if term is None:
        term = db.convert_term(g_course.term)
        session.add(term)

    return term
