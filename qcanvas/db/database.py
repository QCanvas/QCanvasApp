import pathlib
import platform
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Sequence, MutableSequence, Any

from sqlalchemy import ForeignKey, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, MappedAsDataclass

import qcanvas.util.tree_util as tree
from qcanvas.util.tree_util import HasColumnData


class PageLike:
    @property
    def content(self) -> str | None:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def id(self) -> str:
        raise NotImplementedError()

    @property
    def resources(self) -> MutableSequence["Resource"]:
        raise NotImplementedError()

    @property
    def course_id(self) -> str:
        raise NotImplementedError()

    @course_id.setter
    def course_id(self, value: str):
        raise NotImplementedError()

    @property
    def updated_at(self) -> datetime:
        raise NotImplementedError()


class Base(AsyncAttrs, DeclarativeBase):
    pass


def default_assignment_module(module: "Module") -> bool:
    result = module.name.lower() in ["assessments", "assessment"]

    return result


class GroupByPreference(Enum):
    GROUP_BY_PAGES = 0
    GROUP_BY_MODULES = 1

class CoursePreferences(Base):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    local_name: Mapped[Optional[str]]
    files_group_by_preference: Mapped["GroupByPreference"] = mapped_column(default=GroupByPreference.GROUP_BY_PAGES)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="preferences")


class Course(MappedAsDataclass, Base, init=False):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(primary_key=True)

    term_id: Mapped[str] = mapped_column(ForeignKey("terms.id"))
    term: Mapped["Term"] = relationship(back_populates="courses")

    preferences: Mapped["CoursePreferences"] = relationship(back_populates="course")

    name: Mapped[str]

    modules: Mapped[List["Module"]] = relationship(back_populates="course")
    module_items: Mapped[List["ModuleItem"]] = relationship(back_populates="course")
    assignments: Mapped[List["Assignment"]] = relationship(back_populates="course")
    resources: Mapped[List["Resource"]] = relationship(back_populates="course")

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

    def __init__(self, id: str, name: str, end_at: Optional[datetime], start_at: Optional[datetime]):
        super().__init__()
        self.id = id
        self.name = name
        self.end_at = end_at
        self.start_at = start_at

    def __hash__(self):
        return hash(self.id) ^ hash(self.end_at) ^ hash(self.start_at) ^ hash(self.name)


class Module(MappedAsDataclass, Base, tree.HasText, init=False):
    __tablename__ = "modules"
    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="modules")

    name: Mapped[str]

    items: Mapped[List["ModuleItem"]] = relationship(back_populates="module", order_by="ModuleItem.position")

    @property
    def text(self) -> str:
        return self.name


class ResourceToModuleItemAssociation(MappedAsDataclass, Base):
    __tablename__ = "resource_to_moduleitem"
    module_item_id: Mapped[str] = mapped_column(ForeignKey("module_items.id"), primary_key=True)
    resource_id: Mapped[str] = mapped_column(ForeignKey("resources.id"), primary_key=True)


class ResourceToAssignmentAssociation(MappedAsDataclass, Base):
    __tablename__ = "resource_to_assignment"
    assignment_id: Mapped[str] = mapped_column(ForeignKey("assignments.id"), primary_key=True)
    resource_id: Mapped[str] = mapped_column(ForeignKey("resources.id"), primary_key=True)


class ResourceState(Enum):
    NOT_DOWNLOADED = 0
    DOWNLOADED = 1
    FAILED = 2

    @staticmethod
    def human_readable(value: "ResourceState"):
        match value:
            case ResourceState.NOT_DOWNLOADED: return "Not downloaded"
            case ResourceState.DOWNLOADED: return "Downloaded"
            case ResourceState.FAILED: return "Failed"

        raise ValueError(value)


class Resource(MappedAsDataclass, Base, tree.HasText):
    __tablename__ = "resources"
    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="resources")

    url: Mapped[str]
    file_name: Mapped[str]  # Human-readable name
    file_size: Mapped[int]
    state: Mapped[ResourceState]
    fail_message: Mapped[Optional[str]]
    date_discovered: Mapped[datetime]

    module_items: Mapped[List["ModuleItem"]] = relationship(secondary=ResourceToModuleItemAssociation.__table__,
                                                            back_populates="resources", order_by="ModuleItem.position")
    assignments: Mapped[List["Assignment"]] = relationship(secondary=ResourceToAssignmentAssociation.__table__,
                                                           back_populates="resources")

    def __init__(self, id: str, url: str, file_name: str, file_size: int,
                 date_discovered: datetime = datetime.now(),
                 fail_message: Optional[str] = None, state=ResourceState.NOT_DOWNLOADED):
        super().__init__()
        self.id = id
        self.url = url
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

    @property
    def text(self) -> str:
        return self.file_name

    @property
    def download_location(self) -> pathlib.Path:
        file_id: str = self.id

        # Colon is illegal in microsoft windows file names
        if platform.system() == "Windows":
            file_id.replace(':', '$')

        return pathlib.Path("download", f"{file_id}@{self.file_name}")


class ModuleItem(MappedAsDataclass, Base, tree.HasText):
    __tablename__ = "module_items"

    id: Mapped[str] = mapped_column(primary_key=True)

    module_id: Mapped[str] = mapped_column(ForeignKey("modules.id"))
    module: Mapped["Module"] = relationship(back_populates="items")

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="module_items")

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    name: Mapped[str]
    position: Mapped[int]
    type: Mapped[str]

    resources: Mapped[List["Resource"]] = relationship(secondary=ResourceToModuleItemAssociation.__table__,
                                                       back_populates="module_items")

    __mapper_args__ = {
        "polymorphic_identity": "module_item",
        "polymorphic_on": "type",
    }

    def __init__(self, id: str, created_at: datetime, updated_at: datetime, name: str):
        super().__init__()

        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name

    @property
    def text(self) -> str:
        return self.name


class ModuleFile(ModuleItem):
    __tablename__ = "module_files"

    id: Mapped[str] = mapped_column(ForeignKey("module_items.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "module_file",
    }

    def __init__(self, id: str, created_at: datetime, updated_at: datetime, name: str):
        super().__init__(id, created_at, updated_at, name)

        self.id = id


class ModulePage(ModuleItem, PageLike):
    __tablename__ = "module_pages"

    id: Mapped[str] = mapped_column(ForeignKey("module_items.id"), primary_key=True)

    content: Mapped[str] = mapped_column()

    __mapper_args__ = {
        "polymorphic_identity": "module_page",
    }

    def __init__(self, id: str, created_at: datetime, updated_at: datetime, name: str, content: str = "Not loaded"):
        super().__init__(id, created_at, updated_at, name)

        self.id = id
        self.content = content

    def __eq__(self, __value):
        if isinstance(__value, ModulePage):
            return self.id == __value.id
        else:
            return super().__eq__(__value)


class Assignment(MappedAsDataclass, Base, PageLike, tree.HasText, init=False):
    __tablename__ = "assignments"

    id: Mapped[str] = mapped_column(primary_key=True)

    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="assignments")

    name: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(Text, repr=False)
    due_at: Mapped[Optional[datetime]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    position: Mapped[int]

    resources: Mapped[List["Resource"]] = relationship(secondary=ResourceToAssignmentAssociation.__table__,
                                                       back_populates="assignments")

    @property
    def content(self) -> str:
        return self.description

    @property
    def text(self) -> str:
        return self.name
