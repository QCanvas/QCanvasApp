from PySide6.QtCore import QMimeDatabase
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyle

_mime_database = QMimeDatabase()
_default_icon = None


def icon_for_filename(file_name: str) -> QIcon:
    """
    Gets the icon for a filename, based on its extension
    Parameters
    ----------
    file_name
        The name of the file
    Returns
    -------
    QIcon
        The icon for the file
    """
    global _default_icon

    for mime_type in _mime_database.mimeTypesForFileName(file_name):
        icon = QIcon.fromTheme(mime_type.iconName())

        # Return the appropriate icon if it's found
        if not icon.isNull():
            return icon

    # Cache the default icon, used when the icon for a file is unknown/not found
    if _default_icon is None:
        _default_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)

    return _default_icon
