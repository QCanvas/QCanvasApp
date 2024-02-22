from datetime import datetime

import qdarktheme

from qcanvas.util.app_settings import settings


def apply_selected_theme() -> None:
    """
    Applies the selected theme from the app's settings
    """
    if settings.theme != "native":
        qdarktheme.setup_theme(
            settings.theme,
            custom_colors=_get_colours()
        )


red_theme = {
    "primary": "e21d31",
    "[light]": {"foreground": "480910", "background": "fcf8f8"},
    "[dark]": {"foreground": "fbdfe2", "background": "231f1f"}
}


def _get_colours() -> dict:
    now = datetime.now()

    if now.year >= 2025:
        print("I certainly hope not")

    if now.month == 3 and now.day == 17:
        # And this is on the weekend...
        return {"primary": "08ff00"}
    elif now.month == 2 and now.day == 14:
        print("Why are you looking at canvas? Don't you have something better to do?")

        # Nobody will ever see this because uni starts around the 20th
        # Too bad, I kinda liked the theme
        return red_theme
    elif now.month == 8 and now.day == 20:
        # Some random day... I just wanted to see the red theme
        return red_theme
    else:
        return {"primary": "FF804F"}
