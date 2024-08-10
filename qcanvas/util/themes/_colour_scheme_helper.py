import logging

from qtpy.QtCore import QObject, Signal, Slot
from qtpy.QtGui import QGuiApplication, Qt

_logger = logging.getLogger(__name__)


def colour_scheme() -> Qt.ColorScheme:
    return QGuiApplication.styleHints().colorScheme()


def is_dark_colour_scheme() -> bool:
    return colour_scheme() == Qt.ColorScheme.Dark


class ColourSchemeChangeEvent(QObject):
    theme_changed = Signal()

    def __init__(self):
        super().__init__(None)
        self._last_theme = colour_scheme()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self._theme_changed)

    @Slot(Qt.ColorScheme)
    def _theme_changed(self, colour_scheme: Qt.ColorScheme) -> None:
        # Ensure the signal isn't fired when there wasn't actually a change
        if colour_scheme != self._last_theme:
            self._last_theme = colour_scheme
            self.theme_changed.emit()


_theme_changed_listener = ColourSchemeChangeEvent()


def colour_scheme_changed() -> Signal:
    global _theme_changed_listener
    return _theme_changed_listener.theme_changed
