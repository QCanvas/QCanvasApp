from typing import Sequence

import qcanvas.db.database as db
from qcanvas.QtVersionHelper.QtCore import QObject, Slot, Qt
from qcanvas.QtVersionHelper.QtWidgets import QStyledItemDelegate, QStyleOptionProgressBar, QApplication, QStyle, \
    QHeaderView, QStyleOptionViewItem, QTreeWidget, QTreeWidgetItem
from qcanvas.util import file_icon_helper
from qcanvas.util.download_pool import DownloadPool


# https://code.whatever.social/questions/1094841/get-human-readable-version-of-file-size#1094933
def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


class FileColumnDelegate(QStyledItemDelegate):
    def __init__(self, tree: QTreeWidget, download_pool: DownloadPool, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.download_pool = download_pool
        self.tree = tree

    def paint(self, painter, option, index) -> None:
        item = self.tree.itemFromIndex(index)

        # Check that the item is actually a file row and not already downloaded
        if not isinstance(item, FileRow) or item.resource.state == db.ResourceState.DOWNLOADED:
            return super().paint(painter, option, index)

        resource = item.resource
        progress = item.download_progres

        if progress == resource.file_size:
            return super().paint(painter, option, index)

        # Check that the file is not currently downloading (signaled by progress = -1)
        if progress < 0:
            # Show the state of the file instead (downloaded, failed, not downloaded)
            view_item = QStyleOptionViewItem(option)
            self.initStyleOption(view_item, index)
            view_item.text = db.ResourceState.human_readable(resource.state)

            return QApplication.style().drawControl(QStyle.CE_ItemViewItem, view_item, painter, view_item.widget)
        else:
            # otherwise show progress bar
            progress_bar = QStyleOptionProgressBar()
            progress_bar.rect = option.rect
            progress_bar.minimum = 0
            progress_bar.maximum = resource.file_size
            progress_bar.progress = progress
            # Display download progress as a percentage
            progress_bar.text = "{0:.1f}%".format((progress / resource.file_size) * 100)
            progress_bar.textVisible = True

            QApplication.style().drawControl(QStyle.CE_ProgressBar, progress_bar, painter)


class FileRow(QTreeWidgetItem):
    def __init__(self, resource: db.Resource):
        # Set column names
        super().__init__(
            [
                resource.file_name,
                resource.date_discovered.strftime("%Y-%m-%d"),
                sizeof_fmt(resource.file_size),
            ]
        )

        # Set the icon for this file, displayed in the name column
        self.setIcon(0, file_icon_helper.icon_for_filename(resource.file_name))

        self.resource = resource
        # This is used to pass the download progress value from download_progress_updated to FileColumnDelegate. This way
        # it means we don't have to get the download progress from the DownloadPool a second time with an async function
        # (which is undesirable from an item delegate...). Use -1 to show that the file is not currently downloading.
        self.download_progres = -1


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
