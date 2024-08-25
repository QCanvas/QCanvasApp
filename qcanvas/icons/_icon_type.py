# Unused
import logging

from qtpy.QtGui import QIcon

_logger = logging.getLogger(__name__)


class ThemeIcon:
    def __init__(self, theme_path: str):
        self._theme_path = theme_path
        self._icon = None

    @property
    def icon(self) -> QIcon:
        if self._icon is None:
            self._icon = QIcon.fromTheme(self._theme_path)

        return self._icon

    @property
    def theme_path(self) -> str:
        return self._theme_path

    def __hash__(self) -> int:
        return hash(self._theme_path)


class UniversalIcon(ThemeIcon):
    def __init__(self, theme_path: str, full_path: str):
        super().__init__(theme_path)
        self._full_path = full_path

    @property
    def full_path(self) -> str:
        return self._full_path

    def __hash__(self) -> int:
        return hash(self._theme_path) ^ hash(self.full_path)


AnyIcon = UniversalIcon | ThemeIcon
