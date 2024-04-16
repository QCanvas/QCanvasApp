from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QStandardItem

from qcanvas import db as db


class CourseNode(QStandardItem, QObject):
    name_changed = Signal(db.Course, str)

    def __init__(self, course: db.Course):
        QObject.__init__(self)
        QStandardItem.__init__(self, course.preferences.local_name or course.name)
        self.course = course

    def setData(self, value, role=...):
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
