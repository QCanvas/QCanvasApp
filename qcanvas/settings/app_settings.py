from PySide6.QtCore import QSettings
from packaging.version import Version

from qcanvas.settings.mapped_setting import MappedSetting
from qcanvas.settings.theme_setting import ThemeSetting


class _AppSettings:
    """
    Attributes
    ----------
    settings : QSettings
        Primary settings map for client settings
    auxiliary : QSettings
        Secondary settings map for settings which aren't related to canvas/panopto client functionality
    ignored_update
        If there is an update available and the user chooses not to update, then that version will be stored in here and
        the user will not be asked to update to that version again
    geometry
        Used to restore the main window position when it is re-opened
    window_state
        Used to restore the main window position when it is re-opened
    theme
        The theme of the app
    canvas_url
        The canvas url
    api_key
        The api key for canvas
    """

    settings = QSettings("QCanvas", "client")
    auxiliary = QSettings("QCanvas", "ui")

    canvas_url: MappedSetting[str] = MappedSetting(settings, "canvas_url")
    panopto_url: MappedSetting[str] = MappedSetting(settings, "panopto_url")
    api_key: MappedSetting[str] = MappedSetting(settings, "api_key")

    ignored_update: MappedSetting[Version] = MappedSetting(auxiliary, "ignored_update")
    theme: ThemeSetting = ThemeSetting(auxiliary)
    geometry = MappedSetting(auxiliary, "geometry")
    window_state = MappedSetting(auxiliary, "window_state")


# Global _AppSettings instance
settings = _AppSettings()
