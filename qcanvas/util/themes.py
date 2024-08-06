import logging

import qdarktheme
from qtpy.QtWidgets import QApplication, QStyleFactory

_logger = logging.getLogger(__name__)

default_theme = "auto"


def ensure_theme_is_valid(theme: str) -> str:
    if theme not in ["auto", "light", "dark", "native"]:
        return default_theme
    else:
        return theme


def apply(theme: str) -> None:
    theme = ensure_theme_is_valid(theme)

    if theme != "native":
        QApplication.setStyle(QStyleFactory.create("Fusion"))

        qdarktheme.setup_theme(
            theme,
            custom_colors={"primary": "e02424"},
        )
