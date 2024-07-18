import logging
import platform
import sys
from pathlib import Path

import platformdirs
from qtpy.QtCore import QDir, QSettings

_logger = logging.getLogger(__name__)

_is_running_on_windows = platform.system() == "Windows"
_is_running_on_linux = platform.system() == "Linux"
_is_running_as_pyinstaller = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def client_settings() -> QSettings:
    if _is_running_as_pyinstaller and _is_running_on_windows:
        return QSettings(
            str(Path(QDir.homePath()) / ".config" / "QCanvasTeam" / "canvas.ini"),
            QSettings.Format.IniFormat,
        )
    else:
        return QSettings("QCanvasTeam", "QCanvas")


def root() -> Path:
    root_path = Path()

    if _is_running_as_pyinstaller:
        root_path = platformdirs.user_data_path("QCanvasReborn", "QCanvasTeam")

    _logger.debug("Root path %s", root_path.absolute())
    return root_path


def ui_storage() -> Path:
    return root() / ".UI"


def data_storage() -> Path:
    return root() / ".DATA"
