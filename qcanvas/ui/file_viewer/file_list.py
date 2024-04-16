from typing import Sequence

from PySide6.QtCore import QObject, Slot, Qt
from PySide6.QtWidgets import QHeaderView, QTreeWidget, QTreeWidgetItem

import qcanvas.db.database as db
from qcanvas.ui.file_viewer.file_column_delegate import FileColumnDelegate
from qcanvas.ui.file_viewer.file_row import FileRow
from qcanvas.util.download_pool import DownloadPool


class FileList(QTreeWidget):
    def __init__(self, download_pool: DownloadPool, parent: QObject | None = None):
        super().__init__(parent)
        self._setup_header()

        # Keep a map of file ids to rows, so we can actually update the download column using a file id.
        # This has to be a list or else files that are in multiple modules/pages will not be updated properly on the tree
        self.row_id_map: dict[str, list[FileRow]] = {}
        self.download_pool = download_pool
        self.setAlternatingRowColors(True)
        # Add the download column renderer
        self.setItemDelegateForColumn(3, FileColumnDelegate(tree=self, download_pool=download_pool, parent=None))

        # Connect download update events
        self.download_pool.download_progress_updated.connect(self._file_download_progress_update)
        self.download_pool.download_failed.connect(self._file_download_failed_update)

    @Slot(str, int)
    def _file_download_progress_update(self, resource_id: str, progress: int):
        # Ignore files that aren't in this tree
        if resource_id not in self.row_id_map:
            return

        rows = self.row_id_map[resource_id]

        # Update each row that maps to this file.
        # Note that a file may belong to multiple modules or pages
        for row in rows:
            # Update the progress
            row.download_progres = progress

            # Get the download column for the relevant item
            index = self.indexFromItem(row, 3)

            # Update the download column
            self.model().dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole)

    @Slot(str)
    def _file_download_failed_update(self, resource_id: str):
        if resource_id not in self.row_id_map:
            return

        rows = self.row_id_map[resource_id]

        for row in rows:
            # Get the download column for the relevant item
            index = self.indexFromItem(row, 3)

            # Update the download column
            self.model().dataChanged.emit(index, index, Qt.ItemDataRole.DisplayRole)

    def _setup_header(self):
        self.setColumnCount(4)
        self.setHeaderLabels(["Name", "Date Found", "Size", "Download"])

        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        # Make the download progress column not try to take up all remaining space in the tree, as it just looks weird
        # and decreases room for more important data
        header.setStretchLastSection(0)

    def load_items(self, items: Sequence[db.ModuleItem | db.Module]):
        self.clear()

        groups = []

        for item in items:
            # Get the resources depending on the type of the item
            if isinstance(item, (db.PageLike, db.ModuleItem)):
                resources = item.resources
            elif isinstance(item, db.Module):
                resources = []

                for module_item in item.items:
                    resources.extend(module_item.resources)
            else:
                continue

            # Avoid adding groups with no files in them, it just adds clutter
            if len(resources) == 0:
                continue

            # Create the group node for this item
            group_node = QTreeWidgetItem([item.name])

            # fixme this does not remove duplicate files e.g. when on module groups

            for resource in resources:
                row = FileRow(resource)

                # Put the file into the row id map so we can use the file id provided by download_progress_updated
                # and such to update the download progress in the tree
                if resource.id not in self.row_id_map:
                    self.row_id_map[resource.id] = [row]
                else:
                    self.row_id_map[resource.id].append(row)

                # Add the row to the group
                group_node.addChild(row)

            # Add the module/page to the list
            groups.append(group_node)

        # Add all the items and expand them
        self.insertTopLevelItems(0, groups)
        self.expandAll()

    def clear(self):
        super().clear()
        self._setup_header()
        self.row_id_map.clear()
