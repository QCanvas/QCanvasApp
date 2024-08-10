import logging
from enum import Enum

_logger = logging.getLogger(__name__)


class SelectedTheme(Enum):
    AUTO = 0
    NATIVE = 1
    OVERRIDE = 2
