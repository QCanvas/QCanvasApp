from datetime import datetime
from enum import Enum
from typing import List, Optional

import sqlalchemy
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, MappedAsDataclass


class Base(AsyncAttrs, DeclarativeBase):
    pass


# Checks:
# 0. tablename
# 1. Correct init=False
# 2. selectin loading for list columns
# 3. joined loading for backreferences
# 4. cascade delete
# 5. primary key

class Course(MappedAsDataclass, Base):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(primary_key=True)
    # legacy_id: Mapped[str]

    term_id: Mapped[str] = mapped_column(ForeignKey("terms.id"))
    term: Mapped["Term"] = relationship(back_populates="courses")

    name: Mapped[str]
    local_name: Mapped[Optional[str]]

    modules: Mapped[List["Module"]] = relationship(back_populates="course")
    module_items: Mapped[List["ModuleItem"]] = relationship(back_populates="course")
    assignments: Mapped[List["Assignment"]] = relationship(back_populates="course")
    resources: Mapped[List["Resource"]] = relationship(back_populates="course")

    def __init__(self, id: str, name: str, local_name: Optional[str]):
        super().__init__()

        self.id = id
        self.name = name
        self.local_name = local_name


class Term(MappedAsDataclass, Base):
    """
    A term object.
    Each course belongs to a term.

    Attributes
    ----------
    name: str
        Name of the term
    start_at: Optional[datetime]
        Date the term starts
        Will be null for the 'default term'.
    end_at: Optional[datetime]
        Date the term ends.
        Will be null for the 'default term'.
    courses: list[Course]
        *Not required in constructor.*
        List of courses that belong to this term.
    """

    __tablename__ = "terms"
    id: Mapped[str] = mapped_column(primary_key=True)

    end_at: Mapped[Optional[datetime]]
    start_at: Mapped[Optional[datetime]]
    name: Mapped[str]

    courses: Mapped[List["Course"]] = relationship(back_populates="term", cascade="all, delete")

    def __init__(self, id : str, name: str, end_at: Optional[datetime], start_at: Optional[datetime]):
        super().__init__()
        self.id = id
        self.name = name
        self.end_at = end_at
        self.start_at = start_at


class Module(MappedAsDataclass, Base):
    __tablename__ = "modules"
    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="modules")

    name: Mapped[str]

    items: Mapped[List["ModuleItem"]] = relationship(back_populates="module")
    # resources : Mapped[List]

    def __init__(self, id : str, name : str):
        super().__init__()
        self.id = id
        self.name = name


resource_to_moduleitem_association_table = Table(
    "resource_to_module_item_table",
    Base.metadata,
    Column("module_item_id", ForeignKey("module_items.id"), primary_key=True),
    Column("resource_id", ForeignKey("resources.id"), primary_key=True)
)

resource_to_assignment_association_table = Table(
    "resource_to_assignment_table",
    Base.metadata,
    Column("assignment_id", ForeignKey("assignments.id"), primary_key=True),
    Column("resource_id", ForeignKey("resources.id"), primary_key=True)
)


class ResourceState(Enum):
    NOT_DOWNLOADED = 0
    DOWNLOADED = 1
    FAILED = 2


class Resource(MappedAsDataclass, Base):
    __tablename__ = "resources"
    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="resources")

    # type: Mapped[str]
    url: Mapped[str]
    friendly_name: Mapped[str]  # Human-readable name
    # todo maybe delete file_name? not sure if it's needed
    file_name: Mapped[str]  # Internal name that references the file on disk
    file_size: Mapped[int]
    state: Mapped[ResourceState]
    fail_message: Mapped[Optional[str]]
    date_discovered: Mapped[datetime]

    module_items: Mapped[List["ModuleItem"]] = relationship(secondary=resource_to_moduleitem_association_table,
                                                            back_populates="resources")
    assignments: Mapped[List["Assignment"]] = relationship(secondary=resource_to_assignment_association_table,
                                                           back_populates="resources")

    # __mapper_args__ = {
    #     "polymorphic_identity": "resource",
    #     "polymorphic_on": "type",
    # }

    def __init__(self, id : str, url: str, friendly_name: str, file_name : str, file_size : int, date_discovered : datetime, fail_message : Optional[str] = None, state = ResourceState.NOT_DOWNLOADED):
        super().__init__()
        self.id = id
        self.url = url
        self.friendly_name = friendly_name
        self.file_name = file_name
        self.file_size = file_size
        self.fail_message = fail_message
        self.state = state
        self.date_discovered = date_discovered

    def __eq__(self, __value):
        if isinstance(__value, ModulePage):
            return self.id == __value.id
        else:
            return super().__eq__(__value)


class ModuleItem(MappedAsDataclass, Base):
    __tablename__ = "module_items"

    id: Mapped[str] = mapped_column(primary_key=True)

    module_id: Mapped[str] = mapped_column(ForeignKey("modules.id"))
    module: Mapped["Module"] = relationship(back_populates="items")

    course_id : Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="module_items")

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    name: Mapped[str]
    type: Mapped[str]

    resources: Mapped[List["Resource"]] = relationship(secondary=resource_to_moduleitem_association_table,
                                                       back_populates="module_items")

    __mapper_args__ = {
        "polymorphic_identity": "module_item",
        "polymorphic_on": "type",
    }

    def __init__(self, id : str, created_at : datetime, updated_at : datetime, name : str):
        super().__init__()

        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name


class ModuleFile(ModuleItem):
    __tablename__ = "module_files"

    id: Mapped[str] = mapped_column(ForeignKey("module_items.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "module_file",
    }

    def __init__(self, id : str, created_at : datetime, updated_at : datetime, name : str):
        super().__init__(id, created_at, updated_at, name)

        self.id = id


class ModulePage(ModuleItem):
    __tablename__ = "module_pages"

    id: Mapped[str] = mapped_column(ForeignKey("module_items.id"), primary_key=True)

    content: Mapped[str] = mapped_column()

    __mapper_args__ = {
        "polymorphic_identity": "module_page",
    }

    def __init__(self, id : str, created_at : datetime, updated_at : datetime, name : str, content : str = "Not loaded"):
        super().__init__(id, created_at, updated_at, name)

        self.id = id
        self.content = content

    def __eq__(self, __value):
        if isinstance(__value, ModulePage):
            return self.id == __value.id
        else:
            return super().__eq__(__value)


class Assignment(MappedAsDataclass, Base):
    __tablename__ = "assignments"

    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="assignments")

    name: Mapped[str]
    description: Mapped[str]
    due_at: Mapped[datetime]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    position: Mapped[int]

    resources: Mapped[List["Resource"]] = relationship(secondary=resource_to_assignment_association_table,
                                                       back_populates="assignments")

    def __init__(self, id : str, name : str, description : str, due_at : datetime, created_at : datetime, updated_at : datetime, position : int):
        super().__init__()

        self.id = id
        self.name = name
        self.description = description
        self.due_at = due_at
        self.created_at = created_at
        self.updated_at = updated_at
        self.position = position

