import logging

from qtpy.QtWidgets import QWidget, QSizePolicy

_logger = logging.getLogger(__name__)


def make_truncatable(widget: QWidget) -> None:
    widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
