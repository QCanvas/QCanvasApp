import logging
from typing import Literal

import qdarktheme
from PySide6.QtCore import QObject, Signal, Property, Slot
from PySide6.QtGui import QGuiApplication, Qt, QIcon
from PySide6.QtWidgets import QStyleFactory, QApplication

type Theme = Literal["native", "auto", "dark", "light"]

_logger = logging.getLogger(__name__)


class _AppTheme(QObject):
    themeChanged = Signal()
    darkModeChanged = Signal()

    def __init__(self):
        super().__init__()
        self._last_system_theme = QGuiApplication.styleHints().colorScheme()
        self._theme: Theme | None = None
        self._dark_mode: bool | None = None

        self.darkModeChanged.connect(self._set_icon_paths)
        QGuiApplication.styleHints().colorSchemeChanged.connect(
            self._on_system_theme_changed
        )

    @Property(bool, notify=darkModeChanged)
    def dark_mode(self) -> bool:
        assert self._theme is not None, "Theme has not been set"
        return self._dark_mode

    @Property(str, notify=themeChanged)
    def theme(self) -> Theme:
        assert self._theme is not None, "Theme has not been set"
        return self._theme

    @theme.setter
    def theme(self, value: str):
        value = ensure_theme_is_valid(value)

        if value != self._theme:
            self._update_theme(value)

    def _update_theme(self, theme: str):
        if theme is None or (theme == self._theme and theme not in ["native", "auto"]):
            return

        was_dark_mode = self._dark_mode

        if theme != "native":
            if theme == "auto":
                self._dark_mode = _is_system_using_dark_mode()
                selected_colour_scheme = "dark" if self._dark_mode else "light"
            else:
                self._dark_mode = theme == "dark"
                selected_colour_scheme = theme

            if was_dark_mode != self._dark_mode:
                qdarktheme.setup_theme(
                    selected_colour_scheme,
                    custom_colors={"primary": "e02424"},
                )

                QApplication.setStyle(QStyleFactory.create("Fusion"))
        else:
            self._dark_mode = _is_system_using_dark_mode()

        if theme != self._theme:
            self._theme = theme
            self.themeChanged.emit()

        if was_dark_mode != self._dark_mode:
            self.darkModeChanged.emit()

    @Slot()
    def _set_icon_paths(self):
        QIcon.setFallbackSearchPaths(
            [":icons/dark" if self._dark_mode else ":icons/light", ":icons/universal"]
        )

    @Slot()
    def _on_system_theme_changed(self, scheme: Qt.ColorScheme):
        if scheme != self._last_system_theme:
            self._last_system_theme = scheme
            self._update_theme(self._theme)


def _is_system_using_dark_mode() -> bool:
    return QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark


def ensure_theme_is_valid(theme_name: str) -> Theme:
    if theme_name not in ["auto", "light", "dark", "native"]:
        return "auto"
    else:
        return theme_name


app_theme = _AppTheme()
