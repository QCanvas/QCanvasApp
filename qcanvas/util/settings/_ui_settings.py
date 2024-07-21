import logging

from qtpy.QtCore import QByteArray, QSettings

from qcanvas.util.settings._mapped_setting import MappedSetting

_logger = logging.getLogger(__name__)

_default_theme = "auto"


def ensure_theme_is_valid(theme: str) -> str:
    if theme not in ["auto", "light", "dark", "native"]:
        return _default_theme
    else:
        return theme


class ThemeSetting(MappedSetting):
    def __init__(self):
        super().__init__(default=_default_theme)

    def __get__(self, instance, owner):
        return ensure_theme_is_valid(super().__get__(instance, owner))

    def __set__(self, instance, value):
        super().__set__(instance, ensure_theme_is_valid(value))


class _UISettings:
    settings = QSettings("QCanvasTeam", "QCanvas")
    theme: ThemeSetting = ThemeSetting()
    last_geometry: MappedSetting[QByteArray] = MappedSetting()
    last_window_state: MappedSetting[QByteArray] = MappedSetting()
