from datetime import datetime
from typing import Sequence, Union, Optional

from qasync import asyncSlot

from qcanvas.QtVersionHelper.QtWidgets import QTreeView
from qcanvas.QtVersionHelper.QtGui import QStandardItemModel, QStandardItem
from qcanvas.QtVersionHelper.QtCore import QItemSelection, Slot, Signal, Qt, QObject, QModelIndex

import qcanvas.db as db
from qcanvas.util.course_indexer import DataManager


class CourseNode(QStandardItem, QObject):
    name_changed = Signal(db.Course, str)

    def __init__(self, course: db.Course):
        QObject.__init__(self)
        QStandardItem.__init__(self, course.preferences.local_name or course.name)
        self.course = course

    def setData(self, value, role = ...):
        if isinstance(value, str):
            value = value.strip()

            if len(value) == 0:
                super().setData(self.course.name, role)
                self.name_changed.emit(self.course, None)
            else:
                super().setData(value, role)
                self.name_changed.emit(self.course, value)
        else:
            super().setData(value, role)


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
        self.model.setHorizontalHeaderLabels(["Course"])

        courses_root = self.model.invisibleRootItem()

        for term, courses in self.group_courses_by_term(courses):
            term_node = QStandardItem(term.name)
            term_node.setEditable(False)

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


