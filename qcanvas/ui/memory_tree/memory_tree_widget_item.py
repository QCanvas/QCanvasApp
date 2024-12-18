import logging
from typing import Optional

from PySide6.QtWidgets import QTreeWidgetItem

_logger = logging.getLogger(__name__)


class MemoryTreeWidgetItem(QTreeWidgetItem):
    def __init__(
        self, id: str, data: Optional[object], strings: Optional[list[str]] = None
    ):
        super().__init__(strings)
        self._id = id
        self.extra_data = data

    @property
    def id(self) -> str:
        return self._id
