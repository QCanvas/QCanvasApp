from datetime import datetime

from qcanvas.net.canvas.legacy_canvas_types import LegacyFile
import qcanvas.queries as gql
import qcanvas.db.database as db
from qcanvas.util.canvas_garbage_remover import remove_garbage_from_title as clean_string


def convert_term(term: gql.Term) -> db.Term:
    return db.Term(
        id=term.q_id,
        name=clean_string(term.name),
        start_at=term.start_at,
        end_at=term.end_at
    )


def convert_course(course: gql.Course) -> db.Course:
    return db.Course(
        id=course.m_id,
        name=clean_string(course.name),
        local_name=clean_string(course.course_nickname)
    )


def convert_assignment(assignment: gql.Assignment) -> db.Assignment:
    return db.Assignment(
        id=assignment.q_id,
        name=clean_string(assignment.name),
        description=assignment.description,
        due_at=assignment.due_at,
        created_at=assignment.created_at,
        updated_at=assignment.updated_at,
        position=assignment.position
    )


def convert_page(page: gql.Page, content: str) -> db.ModulePage:
    return db.ModulePage(
        id=page.m_id,
        content=content,
        created_at=page.created_at,
        updated_at=page.updated_at,
        name=clean_string(page.title)
    )


def convert_file_page(file: gql.File) -> db.ModuleFile:
    return db.ModuleFile(
        id=file.m_id,
        created_at=file.created_at,
        updated_at=file.updated_at,
        name=clean_string(file.display_name)
    )


def convert_file(file: gql.File, file_size: int) -> db.Resource:
    return db.Resource(
        id=str(file.m_id),
        url=file.url,
        file_name=clean_string(file.display_name),
        date_discovered=datetime.now(),
        file_size=file_size
    )


def convert_legacy_file(file: LegacyFile) -> db.Resource:
    return db.Resource(
        id=str(file.id),
        url=file.url,
        file_name=clean_string(file.display_name),
        date_discovered=datetime.now(),
        file_size=file.size
    )


def convert_module(module: gql.Module) -> db.Module:
    return db.Module(
        id=module.q_id,
        name=clean_string(module.name)
    )
