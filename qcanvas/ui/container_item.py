from PySide6.QtGui import QStandardItem

from qcanvas.util import tree_util as tree


class ContainerItem(QStandardItem):
    def __init__(self, data: tree.HasText):
        super().__init__()
        self.content = data
        self.setEditable(False)
        self.setText(data.text)
