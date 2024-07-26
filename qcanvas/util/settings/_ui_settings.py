import logging

from qtpy.QtCore import QByteArray, QSettings

from qcanvas.util.settings._mapped_setting import MappedSetting
from qcanvas.util.themes import default_theme, ensure_theme_is_valid

_logger = logging.getLogger(__name__)


class ThemeSetting(MappedSetting):
    def __init__(self):
        super().__init__(default=default_theme)

    def __get__(self, instance, owner):
        return ensure_theme_is_valid(super().__get__(instance, owner))

    def __set__(self, instance, value):
        super().__set__(instance, ensure_theme_is_valid(value))


class _UISettings:
    settings = QSettings("QCanvasTeam", "QCanvas")
    theme: ThemeSetting = ThemeSetting()
    last_geometry: MappedSetting[QByteArray] = MappedSetting()
    last_window_state: MappedSetting[QByteArray] = MappedSetting()
