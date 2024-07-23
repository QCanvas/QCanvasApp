import logging
from typing import *

from qtpy.QtCore import QItemSelectionModel, Slot
from qtpy.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget

from qcanvas.ui.memory_tree._tree_memory import TreeMemory
from qcanvas.ui.memory_tree.memory_tree_widget_item import MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class MemoryTreeWidget(QTreeWidget):
    def __init__(
        self,
        tree_name: str,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._id_map: dict[str, MemoryTreeWidgetItem] = {}
        self._memory = TreeMemory(tree_name)
        self._suppress_expansion_signals = False
        self._suppress_selection_signal = False

        self.itemExpanded.connect(self._expanded)
        self.itemCollapsed.connect(self._collapsed)

    def reexpand(self) -> None:
        self.scheduleDelayedItemsLayout()

        try:
            self._suppress_expansion_signals = True

            collapsed_ids = self._memory.collapsed_ids

            for widget in self._id_map.values():
                if widget.id not in collapsed_ids:
                    _logger.debug("Re-expand %s", widget.id)
                    self.expand(self.indexFromItem(widget, 0))
        finally:
            self._suppress_expansion_signals = False

    def clear(self):
        super().clear()
        self._id_map.clear()

    def select_ids(self, ids: List[str]) -> bool:
        """
        :returns: True if all ids were still found in the tree, False if one or more was missing
        """
        self._suppress_selection_signal = True

        is_first = True
        all_ids_in_tree = True

        try:
            for widget_id in ids:
                if widget_id in self._id_map:
                    _logger.debug("Selected %s", widget_id)

                    flags = (
                        QItemSelectionModel.SelectionFlag.Rows
                        | QItemSelectionModel.SelectionFlag.Select
                    )

                    if is_first:
                        flags |= QItemSelectionModel.SelectionFlag.Clear

                    self.selectionModel().select(
                        self.indexFromItem(self._id_map[widget_id], 0), flags
                    )
                else:
                    _logger.debug(
                        "Item %s is no longer in the tree, can't select it", widget_id
                    )
                    all_ids_in_tree = False
        finally:
            self._suppress_selection_signal = False

        return all_ids_in_tree

    def insertTopLevelItem(self, index: int, item: QTreeWidgetItem):
        super().insertTopLevelItem(index, item)
        self._add_widget_to_id_map(item)

    def insertTopLevelItems(self, index: int, items: Sequence[QTreeWidgetItem]):
        super().insertTopLevelItems(index, items)
        self._add_widget_to_id_map(items)

    def addTopLevelItems(self, items: Sequence[QTreeWidgetItem]):
        super().addTopLevelItems(items)
        self._add_widget_to_id_map(items)

    def _add_widget_to_id_map(
        self, widget: QTreeWidgetItem | Sequence[QTreeWidgetItem]
    ):
        map_updates = {}
        widget_stack = widget if isinstance(widget, List) else [widget]

        while len(widget_stack) > 0:
            item = widget_stack.pop()

            if isinstance(item, MemoryTreeWidgetItem):
                if item.id in self._id_map or item.id in map_updates:
                    raise ValueError(f"Item with ID {item.id} is already in the tree")

                map_updates[item.id] = item
                _logger.debug("Add %s to map", item.id)

            if item.childCount() > 0:
                widget_stack.extend(
                    [item.child(index) for index in range(0, item.childCount())]
                )

        self._id_map.update(map_updates.items())

    @Slot(QTreeWidgetItem)
    def _expanded(self, item: QTreeWidgetItem):
        if self._suppress_expansion_signals:
            return

        if isinstance(item, MemoryTreeWidgetItem):
            _logger.debug("Expanded %s", item.id)
            self._memory.expanded(item.id)

    @Slot(QTreeWidgetItem)
    def _collapsed(self, item: QTreeWidgetItem):
        if self._suppress_expansion_signals:
            return

        if isinstance(item, MemoryTreeWidgetItem):
            _logger.debug("Collapsed %s", item.id)
            self._memory.collapsed(item.id)
