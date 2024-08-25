import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt

from qcanvas.ui.course_viewer.tabs.file_tab.file_tree import FileTree
from qcanvas.ui.memory_tree import MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class PagesFileTree(FileTree):

    def __init__(self, tree_name: str, *, resource_manager: ResourceManager):
        super().__init__(
            tree_name=f"{tree_name}.pages", resource_manager=resource_manager
        )

    def create_tree_items(
        self, data: db.Course, sync_receipt: SyncReceipt
    ) -> Sequence[MemoryTreeWidgetItem]:
        widgets = []

        for group in data.modules:  # type: db.Module
            if len(group.content_items) == 0:
                continue

            # Init group_widget lazily to prevent creating pointless tree widgets
            group_widget: MemoryTreeWidgetItem | None = None
            items_in_group = set()

            for item in group.content_items:
                resource_widgets = []

                for resource in item.resources:  # type: db.Resource
                    if resource.id not in items_in_group:
                        items_in_group.add(resource.id)

                        if group_widget is None:
                            group_widget = self._create_group_widget(
                                group, sync_receipt
                            )

                        resource_widgets.append(
                            self._create_resource_widget(resource, sync_receipt)
                        )

                if len(resource_widgets) > 0:
                    group_widget.addChildren(resource_widgets)

            if group_widget is not None:
                widgets.append(group_widget)

        return widgets
