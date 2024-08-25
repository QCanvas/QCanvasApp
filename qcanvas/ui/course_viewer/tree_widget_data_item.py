from typing import List, Optional

from qtpy.QtWidgets import QTreeWidgetItem

from qcanvas.ui.memory_tree import MemoryTreeWidgetItem


class TreeWidgetDataItem(QTreeWidgetItem):
    def __init__(
        self, id: str, data: Optional[object], strings: Optional[List[str]] = None
    ):
        super().__init__(strings)
        # Still needs ID because it is used to reselect the item
        self._id = id
        self.extra_data = data

    @property
    def id(self) -> str:
        return self._id


AnyTreeDataItem = TreeWidgetDataItem | MemoryTreeWidgetItem
