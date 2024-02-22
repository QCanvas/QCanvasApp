from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QMenu, QWidget

from qcanvas.util import AppSettings
from qcanvas.util.qaction_helper import create_qaction


def change_theme(theme_name: str):
    AppSettings.theme = theme_name
    AppSettings.apply_selected_theme()


class ThemeSelectionMenu(QMenu):
    def __init__(self, parent: QWidget | None = None):
        super().__init__("Theme", parent)

        action_group = QActionGroup(self)

        light_theme = self._create_action("Light", "light")
        dark_theme = self._create_action("Dark", "dark")
        native_theme = self._create_action("Native (requires restart)", "native")

        actions = [light_theme, dark_theme, native_theme]

        self.addActions(actions)

        for theme in actions:
            action_group.addAction(theme)

    def _create_action(self, text: str, theme_name: str):
        return create_qaction(
            name=text,
            parent=self,
            triggered=lambda: change_theme(theme_name),
            checkable=True,
            checked=AppSettings.theme == theme_name
        )
