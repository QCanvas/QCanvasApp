import random
from typing import Sequence, Any

from qcanvas.QtVersionHelper.QtWidgets import QStyledItemDelegate, QStyleOptionProgressBar, QApplication, QStyle
from qcanvas.QtVersionHelper.QtCore import QModelIndex, QPersistentModelIndex, Qt

import qcanvas.util.tree_util as tree
import qcanvas.db.database as db
from qcanvas.util import file_icon_helper
from qcanvas.util.tree_util import HasColumnData


# https://code.whatever.social/questions/1094841/get-human-readable-version-of-file-size#1094933
def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


class FileContainer(tree.HasColumnData, tree.HasParent):
    def __init__(self, file: db.Resource, parent: tree.HasChildren, index: int):
        self._file = file
        self._parent = parent
        self._index_of_self = index

    def get_column_data(self, column: int, role: int) -> str | None:
        if role == Qt.DisplayRole:
            if column == 0:
                return self._file.file_name
            elif column == 1:
                return self._file.date_discovered.strftime("%Y-%m-%d")
            elif column == 2:
                return sizeof_fmt(self._file.file_size)
        elif role == Qt.DecorationRole:
            if column == 0:
                return file_icon_helper.icon_for_filename(self._file.file_name)

        return None

    @property
    def parent(self) -> Any:
        return self._parent

    @property
    def index_of_self(self) -> int:
        return self._index_of_self


class PageContainer(tree.HasColumnData, tree.HasChildren):
    collapsed: bool = False

    def __init__(self, page: db.ModuleItem):
        self._page = page
        self._children = [FileContainer(file, self, index) for index, file in enumerate(page.resources)]

    def get_column_data(self, column: int, role: int) -> str | None:
        if role == Qt.DisplayRole:
            if column == 0:
                return self._page.name

        return None

    @property
    def children(self) -> Sequence[HasColumnData]:
        return self._children


class PageResourceModel(tree.TreeModel):
    def __init__(self, pages: Sequence[db.ModuleItem | db.PageLike] = []):
        super().__init__()
        self.root = [PageContainer(page) for page in pages if len(page.resources) > 0]

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = None) -> int:
        return 4

    def headerData(self, section, orientation, role=None, *args, **kwargs):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ["Name", "Date Found", "Size", "Download"][section]

    def update_page_list(self, pages: Sequence[db.ModuleItem]):
        self.beginResetModel()
        self.root = [PageContainer(page) for page in pages if len(page.resources) > 0]
        self.endResetModel()


class PageResourceDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if not isinstance(index.internalPointer(), FileContainer):
            return super().paint(painter, option, index)

        style: QStyleOptionProgressBar = QStyleOptionProgressBar()

        style.rect = option.rect
        style.minimum = 0
        style.maximum = 100
        style.progress = 0
        style.text = "Test"
        style.textVisible = True

        QApplication.style().drawControl(QStyle.ControlElement.CE_ProgressBar, style, painter)
