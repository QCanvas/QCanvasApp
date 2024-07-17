import logging
from typing import *

import qcanvas_backend.database.types as db
from PySide6.QtCore import Slot, QObject
from qasync import asyncSlot
from qcanvas_backend.qcanvas import QCanvas
from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtWidgets import *

from qcanvas.ui.memory_tree import MemoryTreeWidget, MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class _CourseTreeItem(MemoryTreeWidgetItem, QObject):
    renamed = Signal(db.Course, str)

    def __init__(self, course: db.Course):
        MemoryTreeWidgetItem.__init__(
            self,
            id=course.id,
            data=course,
            strings=[course.configuration.nickname or course.name],
        )
        QObject.__init__(self)

        self._course = course

        self.setFlags(
            Qt.ItemFlag.ItemIsEditable
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
        )

    def setData(self, column: int, role: int, value: Any):
        if column != 0 or not isinstance(value, str):
            return super().setData(column, role, value)

        value = value.strip()

        if len(value) == 0:
            super().setData(column, role, self._course.name)
            self.renamed.emit(self._course, None)
        else:
            super().setData(column, role, value)
            self.renamed.emit(self._course, value)


class CourseTree(MemoryTreeWidget):
    course_selected = Signal(db.Course)

    def __init__(self, qcanvas: QCanvas, parent: Optional[QWidget] = None):
        super().__init__("course_tree", parent)
        self.setHeaderLabel("Courses")
        self._qcanvas = qcanvas
        self._last_selected: Optional[str] = None
        self._suppress_selection = False
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)

    async def load(self):
        data = await self._qcanvas.get_data()
        widgets = []

        for term in reversed(data.terms):
            term_widget = MemoryTreeWidgetItem(
                id=term.id, data=term, strings=[term.name]
            )
            term_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)

            for course in term.courses:
                course_widget = _CourseTreeItem(course)
                course_widget.renamed.connect(self._on_course_renamed)
                term_widget.addChild(course_widget)

            widgets.append(term_widget)

        self.clear()
        self.addTopLevelItems(widgets)
        self.reexpand()

    def reselect(self):
        self._suppress_selection = True

        try:
            if self._last_selected is not None:
                self.select_ids([self._last_selected])
        finally:
            self._suppress_selection = False

    @Slot()
    def _on_selection_changed(self):
        if self._suppress_selection:
            return

        try:
            selected = self.selectedItems()[0]

            if isinstance(selected, MemoryTreeWidgetItem) and isinstance(
                selected.extra_data, db.Course
            ):
                course = selected.extra_data
                _logger.debug("Selected course %s", course.name)
                self._last_selected = course.id
                self.course_selected.emit(course)
                return
        except IndexError:
            pass

        self._last_selected = None
        self.course_selected.emit(None)

    @asyncSlot()
    async def _on_course_renamed(self, course: db.Course, new_name: str):
        _logger.debug("Rename %s -> %s", course.name, new_name)

        async with self._qcanvas.database.session() as session:
            session.add(course)
            course.configuration.nickname = new_name
