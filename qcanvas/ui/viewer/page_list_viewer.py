from abc import abstractmethod
from typing import Sequence

from bs4 import BeautifulSoup

import qcanvas.db as db
from qcanvas.QtVersionHelper.QtWidgets import QWidget, QTextBrowser, QTreeView, QHBoxLayout
from qcanvas.QtVersionHelper.QtGui import QStandardItemModel
from qcanvas.QtVersionHelper.QtCore import QItemSelection, Slot
from qcanvas.ui.container_item import ContainerItem
from qcanvas.util import canvas_garbage_remover
from qcanvas.util.constants import default_assignments_module_names
from qcanvas.util.course_indexer import resource_helpers
from qcanvas.util.linkscanner import ResourceScanner


class LinkTransformer:
    # This is used to indicate that a "link" is actually a resource. The resource id is concatenated to this string.
    # It just has to be a valid url or qt does not send it to anchorClicked properly
    transformed_url_prefix = "data:,"

    def __init__(self, link_scanners: Sequence[ResourceScanner], files: dict[str, db.Resource]):
        self.link_scanners = link_scanners
        self.files = files

    def transform_links(self, html: str):
        doc = BeautifulSoup(html, 'html.parser')

        for element in doc.find_all(resource_helpers.resource_elements):
            for scanner in self.link_scanners:
                if scanner.accepts_link(element):
                    resource_id = f"{scanner.name}:{scanner.extract_id(element)}"
                    # todo make images actually show on the viewer page if they're downloaded
                    if resource_id in self.files:
                        file = self.files[resource_id]

                        substitute = doc.new_tag(name="a")
                        # Put the file id on the end of the url so we don't have to use the scanners to extract an id again..
                        # The actual url doesn't matter
                        substitute.attrs["href"] = f"{self.transformed_url_prefix}{file.id}"
                        substitute.string = f"{file.file_name} ({db.ResourceState.human_readable(file.state)})"

                        element.replace_with(substitute)
                    else:
                        if element.string is not None:
                            element.string += " (Failed to index)"

                    break

        return str(doc)


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
                html = canvas_garbage_remover.remove_stylesheets_from_html(item.content)
                self.viewer.setHtml(self.link_transformer.transform_links(html))


class PagesViewer(PageLikeViewer):
    def __init__(self, link_transformer: LinkTransformer):
        super().__init__("Pages", link_transformer)

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

    def __init__(self, link_transformer: LinkTransformer):
        super().__init__("Putting the ASS in assignments", link_transformer)

    def _internal_fill_tree(self, course: db.Course):
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
