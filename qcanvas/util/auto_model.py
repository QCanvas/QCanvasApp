from dataclasses import fields, is_dataclass
from typing import Sequence

from PySide6.QtCore import (
    QAbstractListModel,
    QObject,
    QModelIndex,
    Property,
    Signal,
    Slot,
)
from PySide6.QtGui import Qt


class AutoModel[T](QAbstractListModel):
    """
    Automatically generates named roles for a dataclass instance or QObject.
    Emulates the `count` property which QML `ListModel`s have.
    Allows directly accessing the QObject (bypassing this model) item through the `__object` role.
    """

    count_changed = Signal()

    def __init__(
        self, type_: type[T], items: list = None, parent: QObject | None = None
    ):
        super().__init__(parent)
        self._type = type_
        self._items = []
        self._last_count = 0

        self.rowsInserted.connect(self._on_rows_changed)
        self.rowsRemoved.connect(self._on_rows_changed)

        if items:
            self.extend(items)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> any:
        if 0 <= index.row() < self.rowCount():
            item = self._items[index.row()]
            role_name: bytes = self.roleNames()[role]

            if role_name:
                if role == Qt.ItemDataRole.UserRole and role_name == b"__object":
                    return item
                else:
                    return getattr(item, role_name.decode())

    def roleNames(self) -> dict[int, bytes]:
        result = {}

        if is_dataclass(self._type):
            # Expose dataclass fields as roles
            for index, field in enumerate(fields(self._type)):
                result[Qt.ItemDataRole.DisplayRole + index] = field.name.encode()
        elif QObject in self._type.__bases__:
            role_index = Qt.ItemDataRole.DisplayRole
            # Expose qobject properties as roles
            for key, value in vars(self._type).items():
                if isinstance(value, Property):
                    result[role_index] = key.encode()
                    role_index += 1

            # Allow access to the actual QObject
            result[Qt.ItemDataRole.UserRole] = b"__object"

        return result

    def rowCount(self, index=...):
        return len(self._items)

    def append(self, item: T) -> None:
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._items.append(item)
        self.endInsertRows()

    def extend(self, items: Sequence[T]) -> None:
        if not items:
            return

        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount() + len(items) - 1
        )
        self._items.extend(items)
        self.endInsertRows()

    def clear(self) -> None:
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount())
        self._items.clear()
        self.endRemoveRows()

    # Needed for compatibility with the QtQuick ListModel element
    @Property(int, notify=count_changed)
    def count(self) -> int:
        return self._last_count

    @Slot()
    def _on_rows_changed(self):
        if (count := self.rowCount()) != self._last_count:
            self._last_count = count
            self.count_changed.emit()
