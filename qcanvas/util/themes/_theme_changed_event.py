import logging

from qtpy.QtCore import QObject, Signal

_logger = logging.getLogger(__name__)


class ThemeChangedEvent(QObject):
    theme_changed = Signal()


theme_changed_event = ThemeChangedEvent(None)


def theme_changed() -> Signal:
    global theme_changed_event
    return theme_changed_event.theme_changed
