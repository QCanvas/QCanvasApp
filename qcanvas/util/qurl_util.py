import logging
from pathlib import Path

from qtpy.QtCore import QUrl

_logger = logging.getLogger(__name__)


def file_url(path: Path) -> QUrl:
    return QUrl.fromLocalFile(str(path.absolute()))
