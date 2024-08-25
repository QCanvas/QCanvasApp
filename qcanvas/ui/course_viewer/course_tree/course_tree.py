import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import Qt, Signal

from qcanvas import icons
from qcanvas.ui.course_viewer.content_tree import ContentTree
from qcanvas.ui.course_viewer.course_tree._course_icon_generator import (
    CourseIconGenerator,
)
from qcanvas.ui.course_viewer.tree_widget_data_item import TreeWidgetDataItem
from qcanvas.ui.memory_tree import MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class _CourseTreeItem(TreeWidgetDataItem):
    def __init__(self, course: db.Course, owner: "CourseTree"):
        TreeWidgetDataItem.__init__(
            self,
            id=course.id,
            data=course,
            strings=[course.configuration.nickname or course.name],
        )

        self._owner = owner
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
            self._owner.course_renamed.emit(self._course, None)
        else:
            super().setData(column, role, value)
            self._owner.course_renamed.emit(self._course, value)


class CourseTree(ContentTree[Sequence[db.Term]]):
    course_renamed = Signal(db.Course, str)

    def __init__(self):
        super().__init__("course_tree", emit_selection_signal_for_type=db.Course)

        self.ui_setup(
            max_width=250, min_width=150, header_text="Courses", indentation=15
        )

    def create_tree_items(
        self, terms: List[db.Term], sync_receipt: SyncReceipt
    ) -> Sequence[MemoryTreeWidgetItem]:
        widgets = []

        for term in reversed(terms):
            term_widget = self._create_term_widget(term)
            course_icon_generator = CourseIconGenerator(term.id)

            for course in term.courses:
                course_widget = self._create_course_widget(
                    course, course_icon_generator, sync_receipt
                )
                term_widget.addChild(course_widget)

            widgets.append(term_widget)

        return widgets

    def _create_course_widget(
        self,
        course: db.Course,
        course_icon_generator: CourseIconGenerator,
        sync_receipt: SyncReceipt,
    ) -> _CourseTreeItem:
        course_widget = _CourseTreeItem(course, self)
        course_widget.setIcon(0, course_icon_generator.get_icon())

        if sync_receipt.was_updated(course):
            self.mark_as_unseen(course_widget)

        return course_widget

    def _create_term_widget(self, term: db.Term) -> MemoryTreeWidgetItem:
        term_widget = MemoryTreeWidgetItem(id=term.id, data=term, strings=[term.name])
        term_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)
        term_widget.setIcon(0, icons.tree_items.semester)

        return term_widget
