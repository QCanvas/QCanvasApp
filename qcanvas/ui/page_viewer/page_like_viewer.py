from abc import abstractmethod

from PySide6.QtCore import Slot, QItemSelection
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget, QTextBrowser, QTreeView, QHBoxLayout

from qcanvas import db as db
from qcanvas.ui.container_item import ContainerItem
from qcanvas.ui.link_transformer import LinkTransformer
from qcanvas.util.helpers import canvas_sanitiser


class PageLikeViewer(QWidget):
    def __init__(self, header_name: str, link_transformer: LinkTransformer):
        super().__init__()
        self.viewer = QTextBrowser()
        self.viewer.setOpenLinks(False)

        # todo just use QTreeWidget instead
        self.tree = QTreeView()
        self.model = QStandardItemModel()
        self.header_name = header_name
        self.link_transformer = link_transformer

        self.tree.setModel(self.model)
        self.tree.selectionModel().selectionChanged.connect(self.on_item_clicked)
        self.model.setHorizontalHeaderLabels([self.header_name])

        layout = QHBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.viewer)
        layout.setStretch(1, 1)
        self.setLayout(layout)

    def fill_tree(self, data: db.Course):
        self.model.clear()
        self.viewer.clear()
        self._internal_fill_tree(data)
        self.model.setHorizontalHeaderLabels([self.header_name])
        self.tree.expandAll()

    def clear(self):
        self.model.clear()
        self.viewer.clear()
        self.model.setHorizontalHeaderLabels([self.header_name])

    @abstractmethod
    def _internal_fill_tree(self, data: db.Course):
        ...

    @Slot(QItemSelection, QItemSelection)
    def on_item_clicked(self, selected: QItemSelection, deselected: QItemSelection):
        if len(self.tree.selectedIndexes()) == 0:
            return

        node = self.model.itemFromIndex(self.tree.selectedIndexes()[0])

        if isinstance(node, ContainerItem):
            item = node.content

            if isinstance(item, db.PageLike):
                if item.content is None:
                    return

                # todo when a file is finished downloading it would be nice if the page was refreshed to show the state properly
                html = canvas_sanitiser.remove_stylesheets_from_html(item.content)
                self.viewer.setHtml(self.link_transformer.transform_links(html))
