from qcanvas.QtVersionHelper import QT_VERSION

if QT_VERSION == 5:
    # noinspection PyUnresolvedReferences
    from PySide2.QtCore import *
elif QT_VERSION == 6:
    # noinspection PyUnresolvedReferences
    from PySide6.QtCore import *
