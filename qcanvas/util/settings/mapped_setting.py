import logging
from typing import *

from qtpy.QtCore import QSettings

_logger = logging.getLogger(__name__)
T = TypeVar("T")


class MappedSetting(Generic[T]):
    """
    Acts as a proxy for a named value in a QSettings object.
    Stores the value in memory when initialised and updates it accordingly, to protect it from changes on disk.
    """

    def __init__(self, default: T | None = None):
        self.settings_object: QSettings
        self.default = default
        self.value = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value) -> None:
        self.value = value
        self.settings_object.setValue(self.setting_name, value)

    def __set_name__(self, owner, name):
        if hasattr(owner, "settings") and isinstance(owner.settings, QSettings):
            self.settings_object = owner.settings
        else:
            raise AttributeError(
                "Expected owner object to have a 'settings' attribute of type QSettings"
            )

        self.setting_name = name
        self.value = self.settings_object.value(self.setting_name, self.default)
