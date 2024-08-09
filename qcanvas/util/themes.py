import logging

import darkdetect
import qdarktheme
from qtpy.QtGui import QGuiApplication
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

        qdarktheme.setup_theme(
            theme,
            custom_colors={"primary": "e02424"},
        )

        QApplication.setStyle(QStyleFactory.create("Fusion"))

        _logger.debug("darkdetect says: %s", darkdetect.theme())
        _logger.debug("qt says: %s", QGuiApplication.styleHints().colorScheme())
