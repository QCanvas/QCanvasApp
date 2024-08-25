import logging
import os.path

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
    # This must be initialised lazily because the QApplication might not be initialised at this time
    _default_icon: QIcon | None = None
    _icon_for_suffix: dict[str, QIcon] = {}

    def icon_for_filename(file_name: str) -> QIcon:
        global _default_icon

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

        _lazy_init_default_icon()

        # No icon for this type of file was found, return default icon
        _icon_for_suffix[file_suffix] = _default_icon
        return _default_icon

    def _lazy_init_default_icon() -> None:
        global _default_icon

        if _default_icon is None:
            _default_icon = QApplication.style().standardIcon(
                QStyle.StandardPixmap.SP_FileIcon
            )
