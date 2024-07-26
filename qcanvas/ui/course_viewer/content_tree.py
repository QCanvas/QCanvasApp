import logging
from abc import abstractmethod
from typing import *

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt
from qtpy.QtCore import QItemSelection, Signal, Slot
from qtpy.QtWidgets import *

from qcanvas.ui.memory_tree import MemoryTreeWidget, MemoryTreeWidgetItem
from qcanvas.util.basic_fonts import bold_font, normal_font

_logger = logging.getLogger(__name__)

T = TypeVar("T")
U = TypeVar("U", bound=Type["ContentTree"])


class ContentTree(MemoryTreeWidget, Generic[T]):
    item_selected = Signal(object)

    @classmethod
    def create_from_receipt(
        cls: U, course: db.Course, *, sync_receipt: SyncReceipt
    ) -> Type[U]:
        tree = cls(course.id)
        tree.reload(course, sync_receipt=sync_receipt)
        return tree

    def __init__(
        self,
        tree_name: str,
        *,
        emit_selection_signal_for_type: Type,
    ):
        super().__init__(tree_name)
        self._reloading = False
        self._last_selected_id: Optional[str] = None
        self._target_data_type = emit_selection_signal_for_type

        self.selectionModel().selectionChanged.connect(self._selection_changed)

    def ui_setup(
        self,
        *,
        header_text: str | Sequence[str],
        indentation: int = 20,
        max_width: int,
        min_width: int,
    ) -> None:
        if not isinstance(header_text, str) and isinstance(header_text, Sequence):
            self.setHeaderLabels(header_text)
        else:
            self.setHeaderLabel(header_text)

        self.setIndentation(indentation)
        self.setMaximumWidth(max_width)
        self.setMinimumWidth(min_width)

    def reload(self, data: T, *, sync_receipt: SyncReceipt) -> None:
        self._reloading = True

        try:
            self.clear()
            self.addTopLevelItems(self.create_tree_items(data, sync_receipt))
            self.reexpand()
        finally:
            self._reloading = False

        self.reselect()

    def reselect(self) -> None:
        if self._last_selected_id is not None:
            if not self.select_ids([self._last_selected_id]):
                self._clear_selection()

    @abstractmethod
    def create_tree_items(
        self, data: T, sync_receipt: SyncReceipt
    ) -> Sequence[MemoryTreeWidgetItem]: ...

    @Slot(QItemSelection, QItemSelection)
    def _selection_changed(self, _0: QItemSelection, _1: QItemSelection) -> None:
        if self._reloading:
            return

        if len(self.selectedItems()) > 0:
            selected = self.selectedItems()[0]
        else:
            self._clear_selection()
            return

        if self.is_unseen(selected):
            self.mark_as_seen(selected)

        if not isinstance(selected, MemoryTreeWidgetItem):
            self._clear_selection()
            return

        data = selected.extra_data

        if isinstance(data, self._target_data_type):
            if hasattr(data, "id"):
                _logger.debug("id=%s selected", data.id)
                self._last_selected_id = data.id
                self.item_selected.emit(data)
            else:
                raise AttributeError(
                    f"Expected {self._target_data_type.__name__} to have an id attribute"
                )
        else:
            logging.warning(
                "Expected type %s, got %s instead, ignoring",
                self._target_data_type.__name__,
                type(data).__name__,
            )

            self._clear_selection()

    def _clear_selection(self) -> None:
        _logger.debug("Clearing selection")

        self._last_selected_id = None
        self.item_selected.emit(None)

    def is_unseen(self, item: QTreeWidgetItem) -> bool:
        return item.font(0).bold()

    def mark_as_unseen(self, item: QTreeWidgetItem) -> None:
        item.setFont(0, bold_font)

    def mark_as_seen(self, item: QTreeWidgetItem) -> None:
        item.setFont(0, normal_font)
