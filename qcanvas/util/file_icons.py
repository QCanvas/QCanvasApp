import logging
import os.path

import cachetools
from PySide6.QtCore import QFileInfo, QMimeDatabase
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFileIconProvider, QStyle

import qcanvas.util.runtime as runtime

_logger = logging.getLogger(__name__)

# Windows and linux have different ways of doing this
if runtime.is_running_on_windows:
    _icon_provider = QFileIconProvider()

    def icon_for_filename(file_name: str) -> QIcon:
        return _icon_provider.icon(QFileInfo(file_name))

else:
    _mime_database = QMimeDatabase()
    _icon_for_suffix: dict[str, QIcon] = {}

    def icon_for_filename(file_name: str) -> QIcon:
        file_suffix = os.path.splitext(file_name)[1]

        # Check if we already know what icon this file type has
        if file_suffix in _icon_for_suffix:
            return _icon_for_suffix[file_suffix]

        # Try to find an icon for this file type
        for mime_type in _mime_database.mimeTypesForFileName(file_name):
            icon = QIcon.fromTheme(mime_type.iconName())

            if not icon.isNull():
                _icon_for_suffix[file_suffix] = icon
                return icon

        # No icon for this type of file was found, use default icon
        icon = _default_icon()
        _icon_for_suffix[file_suffix] = icon
        return icon

    @cachetools.cached(cachetools.LRUCache(maxsize=1))
    def _default_icon() -> QIcon:
        return QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
