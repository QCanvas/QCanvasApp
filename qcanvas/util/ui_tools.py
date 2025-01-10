from typing import Any, Sequence

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QFont
from PySide6.QtWidgets import (
    QMenu,
    QSizePolicy,
    QLabel,
    QWidget,
    QFormLayout,
    QDockWidget,
    QLayout,
    QHBoxLayout,
    QVBoxLayout,
)


def font(*, point_size: float | int | None = None, bold: bool | None = None) -> QFont:
    _font = QFont()

    if point_size is not None:
        if isinstance(point_size, int):
            _font.setPointSize(point_size)
        elif isinstance(point_size, float):
            _font.setPointSizeF(point_size)
        else:
            raise TypeError("point_size")

    if bold is not None:
        _font.setBold(bold)

    return _font


_bold = font(bold=True)


def label(text: str, *, font: QFont = None, allow_truncation: bool = False) -> QLabel:
    _label = QLabel(text)

    if font is not None:
        _label.setFont(font)

    if allow_truncation:
        _label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)

    return _label


def bold_label(text: str, *, allow_truncation: bool = False) -> QLabel:
    return label(text, allow_truncation=allow_truncation, font=_bold)


def form_layout(
    rows: dict[str, QWidget], label_font: QFont | None = _bold, label_suffix: str = ":"
) -> QFormLayout:
    layout = QFormLayout()

    for name, widget in rows.items():
        if label_font:
            layout.addRow(label(name + label_suffix, font=label_font), widget)
        else:
            layout.addRow(name + label_suffix, widget)

    return layout


def size(width: int, height: int):
    return QSize(width, height)


def dock_widget(
    *,
    widget: QWidget,
    title: str | None = None,
    hide: bool = False,
    name: str | None = None,
    min_size: QSize | None = None,
    features: QDockWidget.DockWidgetFeature | None = None,
    parent: QWidget | None = None,
) -> QDockWidget:
    dock = QDockWidget(title, parent)
    dock.setWidget(widget)

    if name is not None:
        dock.setObjectName(name)

    if min_size is not None:
        dock.setMinimumSize(min_size)

    if features is not None:
        dock.setFeatures(features)

    if hide:
        dock.hide()

    return dock


def widget(layout: QLayout) -> QWidget:
    widget = QWidget()
    widget.setLayout(layout)
    return widget


def hbox(*items: QWidget | QLayout) -> QHBoxLayout:
    _add_layout_items(layout := QHBoxLayout(), items)
    return layout


def vbox(*items: QWidget | QLayout) -> QVBoxLayout:
    _add_layout_items(layout := QVBoxLayout(), items)
    return layout


def _add_layout_items(layout: QLayout, items: Sequence[QWidget | QLayout]):
    for item in items:
        if isinstance(item, QLayout):
            layout.addItem(item)
        else:
            layout.addWidget(item)


def create_qaction(
    *,
    name: str,
    shortcut: QKeySequence | None = None,
    parent: QMenu = None,
    triggered: Any = None,
    checkable: bool | None = None,
    checked: bool | None = None,
    icon: QIcon | QPixmap | None = None,
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

    if icon is not None:
        action.setIcon(icon)

    return action
