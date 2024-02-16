from abc import abstractmethod

import qcanvas.db as db
from qcanvas.QtVersionHelper.QtWidgets import QWidget, QTextBrowser, QTreeView, QHBoxLayout
from qcanvas.QtVersionHelper.QtGui import QStandardItemModel
from qcanvas.QtVersionHelper.QtCore import QItemSelection, Slot
from qcanvas.ui.container_item import ContainerItem
from qcanvas.util import canvas_garbage_remover
from qcanvas.util.constants import default_assignments_module_names


class PageLikeViewer(QWidget):
    def __init__(self, header_name : str):
        super().__init__()
        self.viewer = QTextBrowser()
        self.tree = QTreeView()
        self.model = QStandardItemModel()
        self.header_name = header_name

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


    @abstractmethod
    def _internal_fill_tree(self, data: db.Course):
        ...

    @Slot(QItemSelection, QItemSelection)
    def on_item_clicked(self, selected: QItemSelection, deselected: QItemSelection):
        if len(selected.indexes()) == 0:
            return

        node = self.model.itemFromIndex(selected.indexes()[0])

        if isinstance(node, ContainerItem):
            item = node.content

            if isinstance(item, db.PageLike):
                if item.content is None:
                    return

                self.viewer.setHtml(canvas_garbage_remover.remove_stylesheets_from_html(item.content))


class PagesViewer(PageLikeViewer):
    def __init__(self):
        super().__init__("Pages")

    def _internal_fill_tree(self, course: db.Course):
        root = self.model.invisibleRootItem()

        for module in course.modules:
            if module.name.lower() in default_assignments_module_names:
                continue

            module_node = ContainerItem(module)

            for module_item in list[db.ModuleItem](module.items):
                module_node.appendRow(ContainerItem(module_item))

            root.appendRow(module_node)


class AssignmentsViewer(PageLikeViewer):

    def __init__(self):
        super().__init__("Putting the ASS in assignments")

    def _internal_fill_tree(self,  course: db.Course):
        root = self.model.invisibleRootItem()

        default_assessments_module = None

        for module in course.modules:
            if module.name.lower() in default_assignments_module_names:
                default_assessments_module = module
                break

        if default_assessments_module is not None:
            for module_item in default_assessments_module.items:
                root.appendRow(ContainerItem(module_item))

        for assignment in course.assignments:
            root.appendRow(ContainerItem(assignment))
