from typing import Any, Sequence, TypeVar, Generic, Optional

from qcanvas.QtVersionHelper.QtCore import QAbstractItemModel, QModelIndex, Qt, QPersistentModelIndex
from qcanvas.QtVersionHelper.QtWidgets import QWidget
from .model_helpers import HasColumnData, HasParent, HasChildren

T = TypeVar("T")

# todo comment this
class TreeModel(QAbstractItemModel, Generic[T]):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.root: Sequence[T] = []

    def get_item(self, index: QModelIndex | QPersistentModelIndex) -> object:
        if index.isValid():
            return index.internalPointer()

        return self.root

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = ...) -> Any:
        if not index.isValid():
            return None

        item = self.get_item(index)

        if isinstance(item, HasColumnData):
            return item.get_column_data(index.column(), role)
        else:
            return None

    def index(self, row: int, column: int, parent: QModelIndex | QPersistentModelIndex = ...) -> QModelIndex:
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parent_item = self.get_item(parent)

        if isinstance(parent_item, HasChildren):
            parent_list = parent_item.children
        elif isinstance(parent_item, Sequence):
            parent_list = parent_item
        else:
            raise TypeError(
                f"Expected parent of item to be Sequence or HasChildren, actually {parent_item.__class__}")

        if row > len(parent_list) or row < 0:
            return QModelIndex()

        return self.createIndex(row, column, parent_list[row])

    def parent(self, child: QModelIndex | QPersistentModelIndex = QModelIndex()) -> QModelIndex:
        if not child.isValid():
            return QModelIndex()

        child_item = self.get_item(child)

        # We don't need to handle the root items here because... they are the root and have no parents

        if isinstance(child_item, HasParent) and child_item.parent is not None:
            return self.createIndex(child_item.index_of_self, 0, child_item.parent)

        return QModelIndex()

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        if parent.isValid() and parent.column() > 0:
            return 0

        parent_item = self.get_item(parent)

        if isinstance(parent_item, HasChildren):
            return len(parent_item.children)
        elif isinstance(parent_item, Sequence):
            return len(parent_item)
        else:
            return 0

    def get_root(self) -> Sequence[T]:
        """
        Returns the list of root level items (i.e. items which have no parents) for the tree
        :return: List of root level items (i.e. items which have no parents) for the tree
        :return: List of root level items (i.e. items which have no parents) for the tree
        """
        return self.root
