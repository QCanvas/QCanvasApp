import logging
import os
from pathlib import Path

import cachetools
import platformdirs
from PySide6.QtCore import QSettings

from qcanvas.util.runtime import (
    is_running_as_compiled,
    is_running_as_flatpak,
    is_running_portable,
)

_logger = logging.getLogger(__name__)


def data_storage() -> Path:
    return root()


def config_storage() -> Path:
    if is_running_portable:
        return root()
    else:
        path = platformdirs.user_config_path("QCanvasTeam", "QCanvas")
        path.mkdir(parents=True, exist_ok=True)
        return path


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
    elif not is_running_portable:
        _logger.warning("Don't know how we're being run? Are you running from source?")

    print("Root path", root_path.absolute())
    _logger.debug("Root path %s", root_path.absolute())
    return root_path
