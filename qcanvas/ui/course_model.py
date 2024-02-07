from typing import Sequence

import qcanvas.db.database as db
from qcanvas.util.tree_util import TreeModel
from qcanvas.QtVersionHelper.QtCore import QModelIndex, QPersistentModelIndex, Qt


class CourseModel(TreeModel[db.Course]):
    def __init__(self, courses : Sequence[db.Course]):
        super().__init__()
        self.root = courses

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = None) -> int:
        return 1

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = None):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ["Name"][section]
