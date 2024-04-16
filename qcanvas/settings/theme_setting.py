from typing import TypeVar

from PySide6.QtCore import QSettings

from qcanvas.settings.mapped_setting import MappedSetting

default_theme = "auto"


def ensure_theme_is_valid(theme: str) -> str:
    """
    Ensures that a theme name is valid.
    If it is invalid, the default theme ("light") is returned
    Parameters
    ----------
    theme
        The theme name
    Returns
    -------
    str
        A valid theme name
    """
    if theme not in ["auto", "light", "dark", "native"]:
        return default_theme
    else:
        return theme


T = TypeVar("T")


class ThemeSetting(MappedSetting):
    def __init__(self, settings_object: QSettings):
        super().__init__(settings_object, "theme", default_theme)

    def __get__(self, instance, owner):
        return ensure_theme_is_valid(super().__get__(instance, owner))

    def __set__(self, instance, value):
        super().__set__(instance, ensure_theme_is_valid(value))
