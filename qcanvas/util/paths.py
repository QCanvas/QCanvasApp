import logging
from pathlib import Path

_logger = logging.getLogger(__name__)


def root():
    return Path()


def ui_storage():
    return root() / ".ui"
