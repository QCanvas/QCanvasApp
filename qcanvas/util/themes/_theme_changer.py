import logging

import qdarktheme
from qtpy.QtCore import Slot
from qtpy.QtWidgets import QApplication, QStyleFactory

from qcanvas.util.themes._colour_scheme_helper import (
    colour_scheme_changed,
    is_dark_colour_scheme,
)
from qcanvas.util.themes._selected_theme import SelectedTheme
from qcanvas.util.themes._theme_changed_event import theme_changed

_logger = logging.getLogger(__name__)

default_theme = "auto"
_is_dark_mode: bool | None = None
_selected_theme: SelectedTheme | None = None


def apply(theme: str) -> None:
    global _is_dark_mode, _selected_theme

    theme = ensure_theme_is_valid(theme)
    was_dark_mode = _is_dark_mode

    if theme != "native":
        if theme == "auto":
            _is_dark_mode = is_dark_colour_scheme()
            _selected_theme = SelectedTheme.AUTO
            selected_colour_scheme = "dark" if _is_dark_mode else "light"
        else:
            selected_colour_scheme = theme
            _selected_theme = SelectedTheme.OVERRIDE
            _is_dark_mode = theme == "dark"

        qdarktheme.setup_theme(
            selected_colour_scheme,
            custom_colors={"primary": "e02424"},
        )

        QApplication.setStyle(QStyleFactory.create("Fusion"))
    else:
        _selected_theme = SelectedTheme.NATIVE
        _is_dark_mode = is_dark_colour_scheme()

    if was_dark_mode != _is_dark_mode:
        theme_changed().emit()


def is_dark_mode() -> bool:
    return _is_dark_mode


def ensure_theme_is_valid(theme: str) -> str:
    if theme not in ["auto", "light", "dark", "native"]:
        return default_theme
    else:
        return theme


@Slot()
def _scheme_changed():
    global _selected_theme, _is_dark_mode

    if _selected_theme == SelectedTheme.AUTO:
        apply("auto")
    elif _selected_theme == SelectedTheme.NATIVE:
        # noinspection PyTestUnpassedFixture
        _is_dark_mode = is_dark_colour_scheme()
        theme_changed().emit()


colour_scheme_changed().connect(_scheme_changed)
