from typing import Sequence

from PySide6.QtWidgets import QGroupBox, QBoxLayout

from qcanvas import db as db
from qcanvas.ui.file_viewer.file_list import FileList
from qcanvas.util.download_pool import DownloadPool


class FileColumn(QGroupBox):
    def __init__(self, column_name, download_pool: DownloadPool):
        super().__init__(title=column_name)

        self.tree = FileList(download_pool)
        self.setLayout(QBoxLayout(QBoxLayout.Direction.TopToBottom))
        self.layout().addWidget(self.tree)

    def load_items(self, items: Sequence[db.ModuleItem | db.Module]):
        self.tree.load_items(items)

    def clear(self):
        self.tree.clear()
