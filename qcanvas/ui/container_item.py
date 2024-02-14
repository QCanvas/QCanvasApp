from qcanvas.QtVersionHelper.QtCore import Qt
from qcanvas.QtVersionHelper.QtGui import QStandardItem

from qcanvas.util import tree_util as tree


class ContainerItem(QStandardItem):
    content: tree.HasText

    def __init__(self, data: tree.HasText):
        super().__init__()
        self.content = data

    def data(self, role=257):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.content.text
