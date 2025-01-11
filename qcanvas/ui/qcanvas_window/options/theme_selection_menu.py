import logging

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QMenu

from qcanvas import icons
from qcanvas.theme import app_theme
import qcanvas.settings as settings

_logger = logging.getLogger(__name__)


class _ThemeAction(QAction):
    def __init__(self, theme_text: str, theme_name: str, parent: QMenu):
        super().__init__(theme_text, parent)
        self._theme_name = theme_name
        self.setCheckable(True)
        self.setChecked(self._theme_name == settings.ui.theme)
        self.triggered.connect(self._change_theme)

    @Slot()
    def _change_theme(self) -> None:
        settings.ui.theme = self._theme_name
        app_theme.theme = self._theme_name


class ThemeSelectionMenu(QMenu):
    def __init__(self, parent: QMenu):
        super().__init__("Theme", parent)

        action_group = QActionGroup(self)

        auto_theme = _ThemeAction("Auto", "auto", self)
        light_theme = _ThemeAction("Light", "light", self)
        dark_theme = _ThemeAction("Dark", "dark", self)
        native_theme = _ThemeAction("Native (requires restart)", "native", self)

        select_theme_actions = [auto_theme, light_theme, dark_theme, native_theme]

        self.addActions(select_theme_actions)
        self.setIcon(icons.options.theme)

        for selection_action in select_theme_actions:
            action_group.addAction(selection_action)
