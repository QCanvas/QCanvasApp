import logging

from PySide6.QtCore import QByteArray, QSettings

from ._mapped_setting import MappedSetting
from qcanvas.theme import ensure_theme_is_valid

_logger = logging.getLogger(__name__)


class ThemeSetting(MappedSetting):
    def __init__(self):
        super().__init__(default="auto")

    def __get__(self, instance, owner):
        return ensure_theme_is_valid(super().__get__(instance, owner))

    def __set__(self, instance, value):
        super().__set__(instance, ensure_theme_is_valid(value))


class _UISettings:
    settings = QSettings("QCanvasTeam", "UI")
    theme: ThemeSetting = ThemeSetting()
    last_geometry: MappedSetting[QByteArray] = MappedSetting()
    last_window_state: MappedSetting[QByteArray] = MappedSetting()
