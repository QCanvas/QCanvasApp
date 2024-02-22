import qdarktheme

from qcanvas.util.app_settings import settings


def apply_selected_theme() -> None:
    """
    Applies the selected theme from the app's settings
    """
    if settings.theme != "native":
        qdarktheme.setup_theme(
            settings.theme,
            custom_colors={"primary": "FF804F"}
        )
