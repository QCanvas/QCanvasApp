from qcanvas.QtVersionHelper.QtCore import QMimeDatabase
from qcanvas.QtVersionHelper.QtGui import QIcon
from qcanvas.QtVersionHelper.QtWidgets import QApplication, QStyle

_mime_database = QMimeDatabase()
_default_icon = None

def icon_for_filename(file_name : str) -> QIcon:
    global _default_icon

    for mime_type in _mime_database.mimeTypesForFileName(file_name):
        icon = QIcon.fromTheme(mime_type.iconName())

        if not icon.isNull():
            return icon

    if _default_icon is None:
        _default_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)

    return _default_icon
