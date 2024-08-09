import logging

from qtpy.QtCore import QFileInfo, QMimeDatabase
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication, QFileIconProvider, QStyle

import qcanvas.util.runtime as runtime

_logger = logging.getLogger(__name__)

# Windows and linux have different ways of doing this
if runtime.is_running_on_windows:
    _icon_provider = QFileIconProvider()

    def icon_for_filename(file_name: str) -> QIcon:
        return _icon_provider.icon(QFileInfo(file_name))

else:
    _mime_database = QMimeDatabase()
    _default_icon = None

    def icon_for_filename(file_name: str) -> QIcon:
        global _default_icon

        for mime_type in _mime_database.mimeTypesForFileName(file_name):
            icon = QIcon.fromTheme(mime_type.iconName())

            if not icon.isNull():
                return icon

        if _default_icon is None:
            _default_icon = QApplication.style().standardIcon(
                QStyle.StandardPixmap.SP_FileIcon
            )

        return _default_icon
