import logging
import os
from pathlib import Path

import cachetools
import platformdirs
from qtpy.QtCore import QSettings

from qcanvas.util.runtime import *

_logger = logging.getLogger(__name__)


def ui_storage() -> Path:
    return root() / ".UI"


def data_storage() -> Path:
    return root()


def client_settings() -> QSettings:
    if is_running_portable:
        return QSettings("QCanvas.ini", QSettings.Format.IniFormat)
    else:
        return QSettings("QCanvasTeam", "QCanvas")


@cachetools.cached(cachetools.LRUCache(maxsize=1))
def root() -> Path:
    root_path = Path()

    if is_running_as_flatpak:
        # Flatpak does not support portable mode
        root_path = Path(os.environ["XDG_DATA_HOME"])
    elif not is_running_portable and is_running_as_compiled:
        root_path = platformdirs.user_data_path("QCanvasReborn", "QCanvasTeam")

    print("Root path", root_path.absolute())
    _logger.debug("Root path %s", root_path.absolute())
    return root_path
