import logging
import platform
import sys
from pathlib import Path
from typing import *

from qcanvas_api_clients.canvas import CanvasClientConfig
from qcanvas_api_clients.panopto import PanoptoClientConfig
from qtpy.QtCore import QSettings, QDir

from qcanvas.util.settings.mapped_setting import MappedSetting

_logger = logging.getLogger(__name__)

_is_running_on_windows = platform.system() == "Windows"
_is_running_as_pyinstaller = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


class _ClientSettings:
    if _is_running_as_pyinstaller and _is_running_on_windows:
        settings = QSettings(
            str(Path(QDir.homePath()) / ".config" / "QCanvasTeam" / "canvas.ini"),
            QSettings.Format.IniFormat,
        )
    else:
        settings = QSettings("QCanvasTeam", "QCanvas")

    canvas_url: MappedSetting[Optional[str]] = MappedSetting(default=None)
    canvas_api_key: MappedSetting[Optional[str]] = MappedSetting(default=None)
    panopto_url: MappedSetting[Optional[str]] = MappedSetting(default=None)

    @property
    def canvas_config(self) -> CanvasClientConfig:
        return CanvasClientConfig(
            api_token=self.canvas_api_key, canvas_url=self.canvas_url
        )

    @property
    def panopto_config(self) -> PanoptoClientConfig:
        return PanoptoClientConfig(panopto_url=self.panopto_url)
