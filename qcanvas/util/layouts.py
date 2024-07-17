import logging
from typing import *

from qtpy.QtCore import Qt
from qtpy.QtWidgets import *

_logger = logging.getLogger(__name__)

T = TypeVar("T")


class GridItem(NamedTuple):
    widget: QWidget
    col_span: int = 1
    row_span: int = 1
    alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft


def layout_widget(layout_type: Type[T], *items: QWidget) -> QWidget:
    widget = QWidget()
    widget.setLayout(layout(layout_type, *items))
    return widget


def layout(layout_type: Type[T], *items: QWidget) -> T:
    result_layout: QLayout = layout_type()

    for item in items:
        result_layout.addWidget(item)

    return result_layout


def grid_layout_widget(grid: List[List[QWidget | GridItem]]) -> QWidget:
    widget = QWidget()
    widget.setLayout(grid_layout(grid))
    return widget


def grid_layout(grid: List[List[QWidget | GridItem]]) -> QGridLayout:
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