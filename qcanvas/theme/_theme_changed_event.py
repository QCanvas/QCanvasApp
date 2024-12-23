from PySide6.QtCore import QObject, Signal


class ThemeChangedEvent(QObject):
    theme_changed = Signal()


theme_changed_event = ThemeChangedEvent(None)


def theme_changed() -> Signal:
    global theme_changed_event
    return theme_changed_event.theme_changed
