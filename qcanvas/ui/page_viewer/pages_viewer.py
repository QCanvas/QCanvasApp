from qcanvas.ui.viewer.page_like_viewer import PageLikeViewer

from qcanvas import db as db
from qcanvas.ui.container_item import ContainerItem
from qcanvas.ui.link_transformer import LinkTransformer
from qcanvas.util.constants import default_assignments_module_names


class PagesViewer(PageLikeViewer):
    def __init__(self, link_transformer: LinkTransformer):
        super().__init__("Pages", link_transformer)

    def _internal_fill_tree(self, course: db.Course):
        root = self.model.invisibleRootItem()

        for module in course.modules:
            if module.name.lower() in default_assignments_module_names:
                continue

            module_node = ContainerItem(module)
            module_node.setSelectable(False)

            for module_item in list[db.ModuleItem](module.items):
                module_node.appendRow(ContainerItem(module_item))

            root.appendRow(module_node)
