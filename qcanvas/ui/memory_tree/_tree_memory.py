import logging
from pathlib import Path
from typing import *

from lightdb import LightDB, Model

from qcanvas.util import paths

_logger = logging.getLogger(__name__)


def _storage_path() -> Path:
    path = paths.ui_storage() / "TREE.DB"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


_state_db = LightDB(str(_storage_path()))


class _TreeState(Model, table="trees", db=_state_db):
    tree_name: str
    collapsed_items: List[str] = []


def _get_or_create_state(name: str) -> _TreeState:
    state = _TreeState.get(tree_name=name)

    if state is None:
        state = _TreeState.create(tree_name=name)
        # Initialise the list here! Or else every instance has the same list object
        state.collapsed_items = []
        # Important or instances will get duplicated data in some cases
        state.save()
        return state
    else:
        return state


class TreeMemory:
    def __init__(self, tree_name: str):
        self._tree_name = tree_name
        self._state = _get_or_create_state(tree_name)

    def is_expanded(self, node_id: str) -> bool:
        return node_id in self._state.expanded_items

    def expanded(self, node_id: str) -> None:
        self.set_expanded(node_id, True)

    def collapsed(self, node_id: str) -> None:
        self.set_expanded(node_id, False)

    def set_expanded(self, node_id: str, expanded: bool) -> None:
        contains = node_id in self._state.collapsed_items

        if expanded and contains:
            self._state.collapsed_items.remove(node_id)
            self._state.save()
        elif not expanded and not contains:
            self._state.collapsed_items.append(node_id)
            self._state.save()

    @property
    def collapsed_ids(self) -> List[str]:
        return self._state.collapsed_items
