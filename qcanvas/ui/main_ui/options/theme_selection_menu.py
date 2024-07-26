import logging

from qtpy.QtCore import Slot
from qtpy.QtGui import QAction, QActionGroup
from qtpy.QtWidgets import QMenu

from qcanvas.util import settings, themes

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
        themes.apply(self._theme_name)


class ThemeSelectionMenu(QMenu):

    def __init__(self, parent: QMenu):
        super().__init__("Theme", parent)

        action_group = QActionGroup(self)

        auto_theme = _ThemeAction("Auto", "auto", self)
        light_theme = _ThemeAction("Light", "light", self)
        dark_theme = _ThemeAction("Dark", "dark", self)
        native_theme = _ThemeAction("Native (requires restart)", "native", self)

        actions = [auto_theme, light_theme, dark_theme, native_theme]

        self.addActions(actions)

        for theme in actions:
            action_group.addAction(theme)
