from datetime import datetime
from typing import Sequence

from PySide6.QtCore import QItemSelection, Slot, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QTreeView
from qasync import asyncSlot

import qcanvas.db as db
from qcanvas.ui.course_viewer.course_node import CourseNode
from qcanvas.util.course_indexer import DataManager


class CourseList(QTreeView):
    course_selected = Signal(db.Course)

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)

    @asyncSlot(db.Course, str)
    async def course_name_changed(self, course: db.Course, name: str):
        course.preferences.local_name = name
        await self.data_manager.update_item(course.preferences)

    def load_course_list(self, courses: Sequence[db.Course]):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Canvas Courses"])

        courses_root = self.model.invisibleRootItem()

        for term, courses in self.group_courses_by_term(courses):
            term_node = QStandardItem(term.name)
            term_node.setEditable(False)
            term_node.setSelectable(False)

            for course in courses:
                course_node = CourseNode(course)
                course_node.name_changed.connect(self.course_name_changed)
                term_node.appendRow(course_node)

            courses_root.appendRow(term_node)

        self.expandAll()

    @staticmethod
    def group_courses_by_term(courses: Sequence[db.Course]):
        courses_grouped_by_term: dict[db.Term, list[db.Course]] = {}

        # Put courses into groups in the above dict
        for course in courses:
            if course.term in courses_grouped_by_term:
                courses_grouped_by_term[course.term].append(course)
            else:
                courses_grouped_by_term[course.term] = [course]

        # Convert the dict item list into a mutable list
        pairs = list(courses_grouped_by_term.items())
        # Sort them by start date, with most recent terms at the start
        pairs.sort(key=lambda x: x[0].start_at or datetime.min, reverse=True)

        return pairs

    @Slot(QItemSelection, QItemSelection)
    def _on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        if len(self.selectedIndexes()) == 0:
            self.course_selected.emit(None)
        else:
            item = self.model.itemFromIndex(self.selectedIndexes()[0])

            if isinstance(item, CourseNode):
                self.course_selected.emit(item.course)
