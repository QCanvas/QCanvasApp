import sgqlc.types
import sgqlc.operation
import graphql.canvas_schema

_schema = graphql.canvas_schema
_schema_root = _schema.canvas_schema

__all__ = ('Operations',)


def query_full_courses():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='FullCourses')
    _op_all_courses = _op.all_courses()
    _op_all_courses.id()
    _op_all_courses.name()
    _op_all_courses.course_nickname()
    _op_all_courses_term = _op_all_courses.term()
    _op_all_courses_term.end_at()
    _op_all_courses_term.start_at()
    _op_all_courses_term.name()
    _op_all_courses_term.id()
    _op_all_courses_assignments_connection = _op_all_courses.assignments_connection()
    _op_all_courses_assignments_connection_nodes = _op_all_courses_assignments_connection.nodes()
    _op_all_courses_assignments_connection_nodes.description()
    _op_all_courses_assignments_connection_nodes.course_id()
    _op_all_courses_assignments_connection_nodes.due_at()
    _op_all_courses_assignments_connection_nodes.created_at()
    _op_all_courses_assignments_connection_nodes.id()
    _op_all_courses_assignments_connection_nodes.name()
    _op_all_courses_assignments_connection_nodes.position()
    _op_all_courses_assignments_connection_nodes.updated_at()
    _op_all_courses_modules_connection = _op_all_courses.modules_connection()
    _op_all_courses_modules_connection_nodes = _op_all_courses_modules_connection.nodes()
    _op_all_courses_modules_connection_nodes.name()
    _op_all_courses_modules_connection_nodes.id()
    _op_all_courses_modules_connection_nodes_module_items = _op_all_courses_modules_connection_nodes.module_items()
    _op_all_courses_modules_connection_nodes_module_items_content = _op_all_courses_modules_connection_nodes_module_items.content()
    _op_all_courses_modules_connection_nodes_module_items_content__as__File = _op_all_courses_modules_connection_nodes_module_items_content.__as__(_schema.File)
    _op_all_courses_modules_connection_nodes_module_items_content__as__File.__typename__()
    _op_all_courses_modules_connection_nodes_module_items_content__as__File._id()
    _op_all_courses_modules_connection_nodes_module_items_content__as__File.display_name()
    _op_all_courses_modules_connection_nodes_module_items_content__as__File.created_at()
    _op_all_courses_modules_connection_nodes_module_items_content__as__File.updated_at()
    _op_all_courses_modules_connection_nodes_module_items_content__as__File.url()
    _op_all_courses_modules_connection_nodes_module_items_content__as__File.size()
    _op_all_courses_modules_connection_nodes_module_items_content__as__File.mime_class()
    _op_all_courses_modules_connection_nodes_module_items_content__as__File.content_type()
    _op_all_courses_modules_connection_nodes_module_items_content__as__Page = _op_all_courses_modules_connection_nodes_module_items_content.__as__(_schema.Page)
    _op_all_courses_modules_connection_nodes_module_items_content__as__Page.__typename__()
    _op_all_courses_modules_connection_nodes_module_items_content__as__Page._id()
    _op_all_courses_modules_connection_nodes_module_items_content__as__Page.title()
    _op_all_courses_modules_connection_nodes_module_items_content__as__Page.updated_at()
    _op_all_courses_modules_connection_nodes_module_items_content__as__Page.created_at()
    return _op


def query_bare_courses():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='BareCourses')
    _op_all_courses = _op.all_courses()
    _op_all_courses.id()
    _op_all_courses.name()
    _op_all_courses.course_nickname()
    _op_all_courses_term = _op_all_courses.term()
    _op_all_courses_term.end_at()
    _op_all_courses_term.start_at()
    _op_all_courses_term.name()
    _op_all_courses_term.id()
    return _op


class Query:
    bare_courses = query_bare_courses()
    full_courses = query_full_courses()


class Operations:
    query = Query
