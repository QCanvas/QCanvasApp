from typing import Any

from qcanvas.QtVersionHelper import QT_VERSION

if QT_VERSION == 5:
    # noinspection PyUnresolvedReferences
    from PySide2.QtGui import *

    # Seemed to have moved packages... make things easier for myself
    # noinspection PyUnresolvedReferences
    from PySide2.QtWidgets import QAction, QActionGroup
elif QT_VERSION == 6:
    # noinspection PyUnresolvedReferences
    from PySide6.QtGui import *


def create_qaction(name: str, shortcut: QKeySequence | None = None, parent: Any = None, triggered: Any = None,
                   checkable: bool | None = None, checked : bool | None = None) -> QAction:
    action = QAction(name)

    if shortcut is not None:
        action.setShortcut(shortcut)

    if parent is not None:
        action.setParent(parent)

    if triggered is not None:
        action.triggered.connect(triggered)

    if checkable is not None:
        action.setCheckable(checkable)

        if checked is not None:
            action.setChecked(checked)

    return action
