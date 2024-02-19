from qcanvas.QtVersionHelper import QT_VERSION

if QT_VERSION == 5:
    # noinspection PyUnresolvedReferences
    from PySide2.QtWidgets import *
elif QT_VERSION == 6:
    # noinspection PyUnresolvedReferences
    from PySide6.QtWidgets import *
