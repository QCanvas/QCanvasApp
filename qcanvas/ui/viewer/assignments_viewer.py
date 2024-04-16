from qcanvas import db as db
from qcanvas.ui.container_item import ContainerItem
from qcanvas.ui.link_transformer import LinkTransformer
from qcanvas.ui.viewer.page_like_viewer import PageLikeViewer
from qcanvas.util.constants import default_assignments_module_names


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
