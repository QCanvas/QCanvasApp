import logging
from typing import *

from qtpy.QtCore import QItemSelectionModel, Slot
from qtpy.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget

from qcanvas.ui.memory_tree.memory import Memory
from qcanvas.ui.memory_tree.memory_tree_widget_item import MemoryTreeWidgetItem

_logger = logging.getLogger(__name__)


class MemoryTreeWidget(QTreeWidget):
    def __init__(self, tree_name: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._id_map: dict[str, MemoryTreeWidgetItem] = {}
        self._memory = Memory(tree_name, parent=self)
        self._selected_ids = []
        self._suppress_expansion_signals = False
        self._suppress_selection_signal = True

        self.itemExpanded.connect(self._expanded)
        self.itemCollapsed.connect(self._collapsed)
        self.selectionModel().selectionChanged.connect(self._selection_changed)

    def reexpand(self) -> None:
        self.scheduleDelayedItemsLayout()

        try:
            self._suppress_expansion_signals = True
            for widget_id in self._memory.expanded_ids:
                _logger.debug("Reexpand %s", widget_id)

                widget = self._id_map.get(widget_id, None)

                if widget is None:
                    continue

                self.expand(self.indexFromItem(widget, 0))
        finally:
            self._suppress_expansion_signals = False

    def clear(self):
        super().clear()
        self._id_map.clear()
        self._selected_ids.clear()

    def select_ids(self, ids: List[str]) -> None:
        self._suppress_selection_signal = True
        self.selectionModel().clearSelection()

        for widget_id in ids:
            if widget_id in self._id_map:
                _logger.debug("Selected %s", widget_id)
                self.selectionModel().select(
                    self.indexFromItem(self._id_map[widget_id], 0),
                    QItemSelectionModel.SelectionFlag.Rows
                    | QItemSelectionModel.SelectionFlag.Select,
                )

        self._suppress_selection_signal = False

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

    @Slot()
    def _expanded(self, item: QTreeWidgetItem):
        if self._suppress_expansion_signals:
            return

        if isinstance(item, MemoryTreeWidgetItem):
            _logger.debug("Expanded %s", item.id)
            self._memory.expanded(item.id)

    @Slot()
    def _collapsed(self, item: QTreeWidgetItem):
        if self._suppress_expansion_signals:
            return

        if isinstance(item, MemoryTreeWidgetItem):
            _logger.debug("Collapsed %s", item.id)
            self._memory.collapsed(item.id)

    @Slot()
    def _selection_changed(self):
        if self._suppress_selection_signal:
            return

        self._selected_ids = [
            x.id for x in self.selectedItems() if isinstance(x, MemoryTreeWidgetItem)
        ]

        _logger.debug(self._selected_ids)
