import logging
from typing import *

from qtpy.QtCore import QObject, Slot
from stones import LmdbStore, stone

from qcanvas.util import paths

_logger = logging.getLogger(__name__)


class Memory(QObject):
    def __init__(self, tree_name: str, parent: Optional[QObject] = None):
        super().__init__(parent)

        self.destroyed.connect(self._destroyed)

        self._tree_name = tree_name
        self._stone = stone(self._get_storage_path(tree_name), LmdbStore)

    @staticmethod
    def _get_storage_path(tree_name: str) -> str:
        path = paths.ui_storage() / "tree_state" / tree_name
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path)

    def is_expanded(self, node_id: str) -> bool:
        return node_id in self._stone

    def expanded(self, node_id: str) -> None:
        self.set_expanded(node_id, True)

    def collapsed(self, node_id: str) -> None:
        self.set_expanded(node_id, False)

    def set_expanded(self, node_id: str, expanded: bool) -> None:
        if expanded:
            self._stone[node_id] = expanded
        else:
            self._stone.pop(node_id, None)

    @property
    def expanded_ids(self) -> List[str]:
        return [item.decode() for item in self._stone.keys()]

    @Slot()
    def _destroyed(self):
        _logger.debug("Closing stone for %s", self._tree_name)
        self._stone.close()
