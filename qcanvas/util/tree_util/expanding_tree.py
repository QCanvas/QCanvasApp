from typing import Any, TypeVar, Sequence, Optional

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker

from qcanvas.QtVersionHelper.QtCore import QModelIndex, Slot, QItemSelectionModel
from qcanvas.QtVersionHelper.QtWidgets import QTreeView, QWidget
from .model_helpers import HasChildren, HasParent
from .tree_model import TreeModel

T = TypeVar("T")


class ExpandingTreeView(QTreeView):
    """
    Provides a way to retain the collapsed or expanded state of tree items after a model reset. Expects the tree's
    model to implement `AbstractItemModelHasListRoot` and any children to implement `HasChildren`. Also provides
    some methods that can be used to get a model index for an arbitrary object in a tree. These will NOT work when
    duplicate objects are present in the tree. Does NOT support multi-selection.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Constructor
        :param session_factory: The session that will be used to update an item's expanded/collapsed state when it is changed
        :param parent: The parent of this treeview
        """
        super().__init__(parent)
        self._connect_expanded_listeners()

    def reexpand(self) -> None:
        """
        Re-expands all items in the tree that have children based on their saved collapsed/expanded state.
        """
        self._disconnect_expanded_listeners()

        try:
            root: Sequence[Any] = self.model().get_root()

            # Go through every item in the root and reexpand it and any children it has
            for index, item in enumerate(root):
                if isinstance(item, HasChildren):
                    self._reexpand_recur(item, self.model().index(index, 0, QModelIndex()))
        finally:
            self._connect_expanded_listeners()

    def _connect_expanded_listeners(self):
        self.expanded.connect(self.tree_item_expanded)
        self.collapsed.connect(self.tree_item_collapsed)

    def _disconnect_expanded_listeners(self):
        self.expanded.disconnect(self.tree_item_expanded)
        self.collapsed.disconnect(self.tree_item_collapsed)

    def _reexpand_recur(self, item: HasChildren, index: QModelIndex) -> None:
        """
        Internal function to expand an item in the tree. Recurs to any children it has.
        :param item: The object to expand in the tree
        :param index: The index of that object
        """
        # Sanity check
        if not isinstance(item, HasChildren):
            raise TypeError("item must be an instance of HasChildren")

        # Expand this item
        self.setExpanded(index, not item.collapsed)

        for child_index, child in enumerate(item.get_children()):
            # Check if the child item can also have children and be collapsed. Also check that it actually has
            # any children.
            if isinstance(child, HasChildren) and len(child.get_children()) > 0:
                # Expand it and any children it has
                self._reexpand_recur(child, self.model().index(child_index, 0, index))

    @Slot()
    def tree_item_expanded(self, index: QModelIndex) -> None:
        """
        Slot that is connected to the tree's `expanded` signal
        :param index: The index that has been expanded
        """
        item = self.model().get_item(index)

        # Update the item's state
        if isinstance(item, HasChildren):
            item.collapsed = False

    @Slot()
    def tree_item_collapsed(self, index: QModelIndex) -> None:
        """
        Slot that is connected to the tree's `collapsed` signal
        :param index: The index that was collapsed
        """
        item = self.model().get_item(index)

        # Update the item's state
        if isinstance(item, HasChildren):
            item.collapsed = True

    def get_path_of_indexes_for_item(self, item: Any) -> list[int]:
        """
        Gets the path of numerical indexes for an arbitrary object in a tree.
        For example, second child of the first item would be [0, 1].

        :param item: The item to find the path for. The item must belong to the tree
        :return: The path to the item as a list of indexes to follow
        """
        path: list[int] = []

        # Keep going until we reach the root
        while isinstance(item, HasParent) and item.parent is not None:
            # Add the index of the item to the path and then go to the parent of that child until there is no parent
            path.insert(0, item.index_of_self)
            item = item.parent

        # Insert the index of the item belonging to the root list to the path
        path.insert(0, self.model().get_root().index(item))

        return path

    def select_object(self, item: Any) -> None:
        """
        Selects an arbitrary item that belongs to the tree. Will not work for branches that have duplicate items.
        :param item: The item to select. Must belong to the tree
        """
        self.select_item_by_path(self.get_path_of_indexes_for_item(item))

    def select_item_by_path(self, item_path: list) -> None:
        """
        Selects an item based on its path
        :param item_path: The path of the item
        """
        selection_model = self.selectionModel()

        # Convert the path to a model index
        # Clear previous selection and select the whole row
        selection_model.select(self.get_model_index_for_path(item_path),
                               QItemSelectionModel.SelectionFlag.ClearAndSelect | QItemSelectionModel.SelectionFlag.Rows)

    def get_model_index_for_path(self, item_path: list[int]) -> QModelIndex:
        """
        Converts an item's path into a QModelIndex
        :param item_path: The path of the item to convert
        :return: The path as a QModelIndex
        """
        model: TreeModel[Any] = self.model()
        # Get the first index
        item_index = item_path.pop(0)
        # Create the base QModelIndex
        model_index = model.index(item_index, 0, QModelIndex())
        # Get the children of the first item
        children = model.get_root()[item_index]

        while len(item_path) > 0:
            # Get the next item
            item_index = item_path.pop(0)
            # Update the QModelIndex
            model_index = model.index(item_index, 0, model_index)

            if len(item_path) > 0:
                # Sanity check
                if not isinstance(children, HasChildren):
                    raise TypeError("Parent object does not have any children but a child was expected")

                # Go to the children of this child next
                children = children.children[item_index]

        return model_index
