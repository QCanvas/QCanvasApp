from PySide6.QtWidgets import QStyledItemDelegate, QTreeWidget, QStyleOptionViewItem, QApplication, QStyle, \
    QStyleOptionProgressBar

from qcanvas.db import database as db
from qcanvas.ui.file_viewer.file_row import FileRow
from qcanvas.util.download_pool import DownloadPool


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
            progress_bar.text = "{0:.0f}%".format((progress / resource.file_size) * 100)
            progress_bar.textVisible = True

            QApplication.style().drawControl(QStyle.CE_ProgressBar, progress_bar, painter)
