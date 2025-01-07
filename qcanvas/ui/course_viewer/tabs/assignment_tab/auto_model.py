from dataclasses import fields, is_dataclass
from typing import Sequence

from PySide6.QtCore import QAbstractListModel, QObject, QModelIndex, Property
from PySide6.QtGui import Qt


class AutoModel[T](QAbstractListModel):
    def __init__(
        self, type_: type[T], items: list = None, parent: QObject | None = None
    ):
        super().__init__(parent)
        self._type = type_
        self._items = []
        if items:
            self.extend(items)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> any:
        if 0 <= index.row() < self.rowCount():
            item = self._items[index.row()]
            role_name: bytes = self.roleNames()[role]

            if role_name:
                return getattr(item, role_name.decode())

    def roleNames(self) -> dict[int, bytes]:
        result = {}

        if is_dataclass(self._type):
            # Expose dataclass fields as roles
            for index, field in enumerate(fields(self._type)):
                result[Qt.ItemDataRole.DisplayRole + index] = field.name.encode()
        elif QObject in self._type.__bases__:
            # Expose qobject properties as roles
            for key, value in vars(self._type).items():
                if isinstance(value, Property):
                    result[Qt.ItemDataRole.DisplayRole + len(result) - 1] = key.encode()

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
