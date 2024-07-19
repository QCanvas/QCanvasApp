import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import QObject, Qt, Signal, Slot
from qtpy.QtWidgets import *

from qcanvas.ui.memory_tree import MemoryTreeWidget, MemoryTreeWidgetItem
from qcanvas.util.basic_fonts import bold_font, normal_font

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
    course_renamed = Signal(db.Course, str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("course_tree", parent)
        self.setHeaderLabel("Courses")
        self._last_selected_id: Optional[str] = None
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)
        # self.setIndentation(15)
        self.setMaximumWidth(250)
        self.setMinimumWidth(150)

    async def reload(
        self, terms: Sequence[db.Term], *, sync_receipt: Optional[SyncReceipt]
    ) -> None:
        await self.load(terms, sync_receipt=sync_receipt)

    async def load(
        self, terms: Sequence[db.Term], *, sync_receipt: Optional[SyncReceipt]
    ) -> None:
        widgets = []

        for term in reversed(terms):
            term_widget = MemoryTreeWidgetItem(
                id=term.id, data=term, strings=[term.name]
            )
            term_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)

            for course in term.courses:
                course_widget = _CourseTreeItem(course)
                course_widget.renamed.connect(self._on_course_renamed)

                is_new = (
                    sync_receipt is not None
                    and course.id in sync_receipt.updated_courses
                )
                if is_new:
                    course_widget.setFont(0, bold_font)

                term_widget.addChild(course_widget)

            widgets.append(term_widget)

        last_id = self._last_selected_id
        self.clear()
        self.addTopLevelItems(widgets)
        self.reexpand()

        if last_id is not None:
            self.select_ids([last_id])

    @Slot()
    def _on_selection_changed(self) -> None:
        try:
            selected = self.selectedItems()[0]

            if isinstance(selected, MemoryTreeWidgetItem) and isinstance(
                selected.extra_data, db.Course
            ):
                if selected.font(0).bold():
                    selected.setFont(0, normal_font)

                course = selected.extra_data
                _logger.debug("Selected course %s", course.name)
                self._last_selected_id = course.id
                self.course_selected.emit(course)
                return
        except IndexError:
            pass

        self._last_selected_id = None
        self.course_selected.emit(None)

    @Slot()
    def _on_course_renamed(self, course: db.Course, new_name: str) -> None:
        self.course_renamed.emit(course, new_name)
