import logging
from typing import Iterable, NamedTuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLayout, QWidget

_logger = logging.getLogger(__name__)


class GridItem(NamedTuple):
    widget: QWidget
    col_span: int = 1
    row_span: int = 1
    alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft


def layout_widget[T](layout_type: type[T], *items: QWidget, **kwargs) -> QWidget:
    widget = QWidget()
    widget.setLayout(layout(layout_type, *items, **kwargs))
    return widget


def layout[T](layout_type: type[T], *items: QWidget | QLayout, **kwargs) -> T:
    result_layout: QLayout = layout_type(**kwargs)

    for item in items:
        if isinstance(item, QLayout):
            result_layout.addItem(item)
        else:
            result_layout.addWidget(item)

    return result_layout


def grid_layout_widget(grid: Iterable[Iterable[QWidget | GridItem]]) -> QWidget:
    widget = QWidget()
    widget.setLayout(grid_layout(grid))
    return widget


def grid_layout(grid: Iterable[Iterable[QWidget | GridItem]]) -> QGridLayout:
    result_layout = QGridLayout()

    for row, row_list in enumerate(grid):
        for col, item in enumerate(row_list):
            if isinstance(item, GridItem):
                result_layout.addWidget(
                    item.widget, row, col, item.row_span, item.col_span, item.alignment
                )
            else:
                result_layout.addWidget(item, row, col)

    return result_layout
