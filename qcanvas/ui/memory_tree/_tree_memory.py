import asyncio
import logging
from pathlib import Path

from aiofile import async_open

from qcanvas.util import paths

_logger = logging.getLogger(__name__)


class TreeMemory:
    def __init__(self, tree_name: str):
        self._tree_name = tree_name
        self._loaded = False
        self._collapsed_items: set[str] = set()

    def load(self, force: bool = False):
        if force or not self._loaded:
            self._loaded = True

            if not self._storage_path.exists():
                # Nothing to do
                return

            # fixme this blocks the event loop, but using aiofile will require significant changes to other
            #  parts of the code to accommodate these methods now being async.
            #  this will really only have any noticeable effect on slow disks, and only ever happens once anyway.
            with open(self._storage_path, "rt") as file:
                lines = file.read().splitlines()
                _logger.debug("Tree % loaded %s", self._tree_name, lines)
                self._collapsed_items.update(lines)

    async def save(self):
        assert self._loaded, "Memory is not loaded yet"

        async with async_open(self._storage_path, "wt") as file:
            await file.write("\n".join(self._collapsed_items))

    def expanded(self, node_id: str) -> None:
        self.set_expanded(node_id, True)

    def collapsed(self, node_id: str) -> None:
        self.set_expanded(node_id, False)

    def set_expanded(self, node_id: str, expanded: bool) -> None:
        self.load()

        if expanded and node_id in self._collapsed_items:
            self._collapsed_items.remove(node_id)
        else:
            self._collapsed_items.add(node_id)

        # hack: avoid blocking the event loop
        asyncio.create_task(self.save())

    @property
    def collapsed_ids(self) -> set[str]:
        assert self._loaded, "Memory not loaded yet"
        return self._collapsed_items

    @property
    def _storage_path(self) -> Path:
        path = (
            paths.data_storage()
            / "tree_state"
            / f"{self._tree_name}_collapsed_items.txt"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
