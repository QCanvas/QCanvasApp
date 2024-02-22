from typing import TypeVar, Generic

from PySide6.QtCore import QSettings
from packaging.version import Version

default_theme = "light"


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


class MappedSetting(Generic[T]):
    def __init__(self, settings_object: QSettings, setting_name: str, default: T | None = None):
        self.settings_object = settings_object
        self.setting_name = setting_name
        self.value = self.settings_object.value(self.setting_name, default)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value) -> None:
        self.value = value
        self.settings_object.setValue(self.setting_name, value)


class ThemeSetting(MappedSetting):
    def __init__(self, settings_object: QSettings):
        super().__init__(settings_object, "theme", default_theme)

    def __get__(self, instance, owner):
        return ensure_theme_is_valid(super().__get__(instance, owner))

    def __set__(self, instance, value):
        super().__set__(instance, ensure_theme_is_valid(value))


class _AppSettings:
    """
    Attributes
    ----------
    settings : QSettings
        Primary settings map for client settings
    auxiliary : QSettings
        Secondary settings map for settings which aren't related to canvas/panopto client functionality
    """

    settings = QSettings("QCanvas", "client")
    auxiliary = QSettings("QCanvas", "ui")

    canvas_url: MappedSetting[str] = MappedSetting(settings, "canvas_url")
    api_key: MappedSetting[str] = MappedSetting(settings, "api_key")

    ignored_update: MappedSetting[Version] = MappedSetting(auxiliary, "ignored_update")
    geometry = MappedSetting(auxiliary, "geometry")
    window_state = MappedSetting(auxiliary, "window_state")
    theme: ThemeSetting = ThemeSetting(auxiliary)


# Global _AppSettings instance
settings = _AppSettings()
