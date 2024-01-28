from datetime import datetime
from enum import Enum
from typing import Union, List, Optional

import sqlalchemy
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, MappedAsDataclass


class Base(DeclarativeBase):
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

    term_id: Mapped[str] = mapped_column(ForeignKey("terms.id"), init=False)
    term: Mapped["Term"] = relationship(back_populates="courses")

    name: Mapped[str]
    local_name: Mapped[str]

    modules: Mapped[List["Module"]] = relationship(back_populates="course", init=False)
    assignments: Mapped[List["Assignment"]] = relationship(back_populates="course", init=False)
    resources: Mapped[List["Resource"]] = relationship(back_populates="course", init=False)


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

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"), init=False)
    course: Mapped["Course"] = relationship(back_populates="modules", init=False)

    name: Mapped[str]

    items: Mapped[List["ModuleItem"]] = relationship(back_populates="module", init=False)
    # resources : Mapped[List]


resource_to_moduleitem_association_table = Table(
    "resource_to_module_item_table",
    Base.metadata,
    Column("module_item_id", ForeignKey("module_items.id"), primary_key=True),
    Column("resource_id", ForeignKey("generic_resources.id"), primary_key=True)
)

resource_to_assignment_association_table = Table(
    "resource_to_assignment_table",
    Base.metadata,
    Column("assignment_id", ForeignKey("assignments.id"), primary_key=True),
    Column("resource_id", ForeignKey("generic_resources.id"), primary_key=True)
)


class ResourceState(Enum):
    NOT_DOWNLOADED = 0
    DOWNLOADED = 1
    FAILED = 2


class Resource(MappedAsDataclass, Base):
    __tablename__ = "generic_resources"
    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"), init=False)
    course: Mapped["Course"] = relationship(back_populates="resources", init=False)

    type: Mapped[str] = mapped_column(init=False)
    url: Mapped[str]
    friendly_name: Mapped[str]  # Human-readable name
    file_name: Mapped[str]  # Internal name that references the file on disk
    file_size: Mapped[int]
    state: Mapped[ResourceState]
    fail_message: Mapped[Optional[str]]
    date_discovered: Mapped[datetime]

    module_items: Mapped[List["ModuleItem"]] = relationship(secondary=resource_to_moduleitem_association_table,
                                                            back_populates="resources", init=False)
    assignments: Mapped[List["Assignment"]] = relationship(secondary=resource_to_assignment_association_table,
                                                           back_populates="resources", init=False)

    __mapper_args__ = {
        "polymorphic_identity": "generic_resource",
        "polymorphic_on": "type",
    }


class ModuleItem(MappedAsDataclass, Base):
    __tablename__ = "module_items"

    id: Mapped[str] = mapped_column(primary_key=True)

    module_id: Mapped[str] = mapped_column(ForeignKey("modules.id"), init=False)
    module: Mapped["Module"] = relationship(back_populates="items", init=False)

    createdAt: Mapped[datetime]
    updatedAt: Mapped[datetime]
    name: Mapped[str]
    type: Mapped[str] = mapped_column(init=False)

    resources: Mapped[List["Resource"]] = relationship(secondary=resource_to_moduleitem_association_table,
                                                       back_populates="module_items")

    __mapper_args__ = {
        "polymorphic_identity": "module_item",
        "polymorphic_on": "type",
    }


class ModuleFile(ModuleItem):
    __tablename__ = "module_files"

    id: Mapped[str] = mapped_column(ForeignKey("module_items.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "module_file",
    }


class ModulePage(ModuleItem):
    __tablename__ = "module_pages"

    id: Mapped[str] = mapped_column(ForeignKey("module_items.id"), primary_key=True)

    content: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "module_page",
    }


class Assignment(MappedAsDataclass, Base):
    __tablename__ = "assignments"

    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"), init=False)
    course: Mapped["Course"] = relationship(back_populates="assignments", init=False)

    name: Mapped[str]
    description: Mapped[str]
    dueAt: Mapped[datetime]
    createdAt: Mapped[datetime]
    updatedAt: Mapped[datetime]
    position: Mapped[int]

    resources: Mapped[List["Resource"]] = relationship(secondary=resource_to_assignment_association_table,
                                                       back_populates="assignments")
