import logging
from pathlib import Path

_logger = logging.getLogger(__name__)


def root() -> Path:
    return Path()


def ui_storage() -> Path:
    return root() / ".UI"


def data_storage() -> Path:
    return root() / ".DATA"
