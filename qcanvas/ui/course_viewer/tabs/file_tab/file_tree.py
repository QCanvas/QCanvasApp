import logging
from enum import Enum
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import QFileInfo, QMimeDatabase, QPoint, Qt, Slot
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import *
from qtpy.QtWidgets import QApplication, QStyle

from qcanvas.ui.course_viewer.content_tree import ContentTree
from qcanvas.ui.memory_tree import MemoryTreeWidgetItem
from qcanvas.util import runtime
from qcanvas.util.ui_tools import create_qaction

_logger = logging.getLogger(__name__)

# Windows and linux have different ways of doing this
if runtime.is_running_on_windows:
    _icon_provider = QFileIconProvider()

    def _icon_for_filename(file_name: str) -> QIcon:
        return _icon_provider.icon(QFileInfo(file_name))

else:
    _mime_database = QMimeDatabase()
    _default_icon = None

    def _icon_for_filename(file_name: str) -> QIcon:
        global _default_icon

        for mime_type in _mime_database.mimeTypesForFileName(file_name):
            icon = QIcon.fromTheme(mime_type.iconName())

            if not icon.isNull():
                return icon

        if _default_icon is None:
            _default_icon = QApplication.style().standardIcon(
                QStyle.StandardPixmap.SP_FileIcon
            )

        return _default_icon


class _Mode(Enum):
    ASSIGNMENTS = 0
    PAGES = 1


_ModeString = Literal["assignments", "pages"]
T = TypeVar("T")


class FileTree(ContentTree[db.Course]):
    @staticmethod
    def create_from_receipt(
        course: db.Course,
        *,
        sync_receipt: SyncReceipt,
        mode: _ModeString,
        resource_manager: ResourceManager,
    ) -> "FileTree":
        tree = FileTree(course.id, mode=mode, resource_manager=resource_manager)
        tree.reload(course, sync_receipt=sync_receipt)
        return tree

    def __init__(
        self, tree_name: str, *, mode: _ModeString, resource_manager: ResourceManager
    ):
        super().__init__(f"{tree_name}.{mode}", emit_selection_signal_for_type=object)
        self._mode = _Mode.PAGES if mode == "pages" else _Mode.ASSIGNMENTS
        self._resource_manager = resource_manager

        self.ui_setup(header_text=["File", "Date"])
        self._adjust_header()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._context_menu)

    def _adjust_header(self) -> None:
        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(False)

    def create_tree_items(
        self, data: db.Course, sync_receipt: SyncReceipt
    ) -> Sequence[MemoryTreeWidgetItem]:
        widgets = []

        groups: list[db.ContentGroup] = (
            data.assignment_groups if self._mode == _Mode.ASSIGNMENTS else data.modules
        )

        for group in groups:
            group_widget = self._create_group_widget(group, sync_receipt)

            for item in group.content_items:
                for resource in item.resources:
                    resource_widget = self._create_resource_widget(
                        resource, sync_receipt
                    )

                    group_widget.addChild(resource_widget)

            widgets.append(group_widget)

        return widgets

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
    ) -> MemoryTreeWidgetItem:
        item_widget = MemoryTreeWidgetItem(
            id=resource.id,
            data=resource,
            strings=[resource.file_name, str(resource.discovery_date.date())],
        )
        item_widget.setIcon(
            0,
            _icon_for_filename(resource.file_name),
        )
        item_widget.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        if sync_receipt.was_updated(resource):
            self.mark_as_unseen(item_widget)

        return item_widget

    @Slot(QPoint)
    def _context_menu(self, point: QPoint) -> None:
        item = self.itemAt(point)

        if item is None or not isinstance(item, MemoryTreeWidgetItem):
            return

        menu = QMenu()
        create_qaction(
            name="Test",
            parent=menu,
            triggered=lambda: print(f"Clicked {item.extra_data.file_name}"),
        )
        menu.addAction("Another thing")

        menu.exec(self.mapToGlobal(point))
