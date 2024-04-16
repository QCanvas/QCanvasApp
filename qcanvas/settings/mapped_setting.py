from typing import Generic

from PySide6.QtCore import QSettings

from qcanvas.settings.theme_setting import T


class MappedSetting(Generic[T]):
    """
    Acts as a proxy for a named value in a QSettings object.
    Stores the value in memory when initialised and updates it accordingly, to protect it from changes on disk.
    """

    def __init__(self, settings_object: QSettings, setting_name: str, default: T | None = None):
        self.settings_object = settings_object
        self.setting_name = setting_name
        self.value = self.settings_object.value(self.setting_name, default)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value) -> None:
        self.value = value
        self.settings_object.setValue(self.setting_name, value)
