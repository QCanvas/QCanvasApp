import logging
from typing import Any

from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import *

_logger = logging.getLogger(__name__)


def make_truncatable(widget: QWidget) -> None:
    widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)


def create_qaction(
    *,
    name: str,
    shortcut: QKeySequence | None = None,
    parent: QMenu = None,
    triggered: Any = None,
    checkable: bool | None = None,
    checked: bool | None = None,
) -> QAction:
    action = QAction(name)

    if shortcut is not None:
        action.setShortcut(shortcut)

    if parent is not None:
        action.setParent(parent)
        parent.addAction(action)

    if triggered is not None:
        action.triggered.connect(triggered)

    if checkable is not None:
        action.setCheckable(checkable)

        if checked is not None:
            action.setChecked(checked)

    return action
