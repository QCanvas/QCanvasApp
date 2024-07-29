import logging
import os
import platform
import sys
from pathlib import Path

import cachetools
import platformdirs
from qtpy.QtCore import QSettings

_logger = logging.getLogger(__name__)

_is_running_on_windows = platform.system() == "Windows"
_is_running_on_linux = platform.system() == "Linux"
_is_running_as_pyinstaller = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
_is_running_as_flatpak = os.environ.get("container", "") == "flatpak"


def client_settings() -> QSettings:
    if _is_running_as_pyinstaller and _is_running_on_windows:
        return QSettings(
            str(platformdirs.user_documents_path() / "QCanvasTeam" / "QCanvas.ini"),
            QSettings.Format.IniFormat,
        )
    else:
        return QSettings("QCanvasTeam", "QCanvas")


@cachetools.cached(cachetools.LRUCache(maxsize=1))
def root() -> Path:
    root_path = Path()

    if _is_running_as_flatpak:
        root_path = Path(os.environ["XDG_DATA_HOME"])
    elif _is_running_as_pyinstaller:
        root_path = platformdirs.user_data_path("QCanvasReborn", "QCanvasTeam")

    print("Root path", root_path.absolute())
    _logger.debug("Root path %s", root_path.absolute())
    return root_path


def ui_storage() -> Path:
    return root() / ".UI"


def data_storage() -> Path:
    return root()
