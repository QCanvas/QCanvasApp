import logging
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import QPoint, Qt, Slot
from qtpy.QtWidgets import *

from qcanvas.ui.course_viewer.content_tree import ContentTree
from qcanvas.ui.course_viewer.tree_widget_data_item import (
    AnyTreeDataItem,
    TreeWidgetDataItem,
)
from qcanvas.ui.memory_tree import MemoryTreeWidgetItem
from qcanvas.util.file_icons import icon_for_filename
from qcanvas.util.ui_tools import create_qaction

_logger = logging.getLogger(__name__)


T = TypeVar("T")


class FileTree(ContentTree[db.Course]):
    @classmethod
    def create_from_receipt(
        cls,
        course: db.Course,
        *,
        sync_receipt: SyncReceipt,
        resource_manager: ResourceManager,
    ) -> "FileTree":
        tree = cls(tree_name=course.id, resource_manager=resource_manager)
        tree.reload(course, sync_receipt=sync_receipt)
        return tree

    def __init__(self, tree_name: str, *, resource_manager: ResourceManager):
        super().__init__(tree_name, emit_selection_signal_for_type=object)
        self._resource_manager = resource_manager

        self.ui_setup(header_text=["File", "Date"])
        self.set_columns_resize_mode(
            [QHeaderView.ResizeMode.Stretch, QHeaderView.ResizeMode.ResizeToContents]
        )

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._context_menu)

    def _create_group_widget(
        self, group: db.ContentGroup, sync_receipt: SyncReceipt
    ) -> MemoryTreeWidgetItem:
        group_widget = MemoryTreeWidgetItem(
            id=group.id, data=group, strings=[group.name]
        )

        group_widget.setFlags(Qt.ItemFlag.ItemIsEnabled)

        if sync_receipt.was_updated(group):
            self.mark_as_unseen(group_widget)

        return group_widget

    def _create_resource_widget(
        self, resource: db.Resource, sync_receipt: SyncReceipt
    ) -> QTreeWidgetItem:
        # fixme the reesource widget items shouls NOT be a memory widget item because they can't be collapsed, but
        #  mostly because the same file can appear in the tree multiple times in different places, which memory tree
        #  can NOT deal with!
        item_widget = TreeWidgetDataItem(
            id=resource.id,
            data=resource,
            strings=[resource.file_name, str(resource.discovery_date.date())],
        )
        item_widget.setIcon(
            0,
            icon_for_filename(resource.file_name),
        )
        item_widget.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        if sync_receipt.was_updated(resource):
            self.mark_as_unseen(item_widget)

        return item_widget

    @Slot(QPoint)
    def _context_menu(self, point: QPoint) -> None:
        item = self.itemAt(point)

        if isinstance(item, AnyTreeDataItem):
            menu = QMenu()
            create_qaction(
                name="Test",
                parent=menu,
                triggered=lambda: print(f"Clicked {item.extra_data.file_name}"),
            )
            menu.addAction("Another thing")

            menu.exec(self.mapToGlobal(point))
