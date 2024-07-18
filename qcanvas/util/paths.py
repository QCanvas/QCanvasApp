import logging
import platform
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths
from qtpy.QtCore import QDir
from qtpy.QtCore import QSettings

_logger = logging.getLogger(__name__)

_is_running_on_windows = platform.system() == "Windows"
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
    if _is_running_as_pyinstaller:
        return Path(
            QStandardPaths.standardLocations(
                QStandardPaths.StandardLocation.AppLocalDataLocation
            )[0]
        )
    else:
        return Path()


def ui_storage() -> Path:
    return root() / ".UI"


def data_storage() -> Path:
    return root() / ".DATA"
