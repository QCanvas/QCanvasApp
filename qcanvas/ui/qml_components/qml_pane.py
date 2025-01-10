from pathlib import Path

from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QGroupBox, QWidget

from qcanvas.theme import app_theme
from qcanvas.util.context_dict import ContextDict
import qcanvas.util.ui_tools as ui


class QmlPane(QGroupBox):
    def __init__(self, qml_path: Path, parent: QWidget | None = None):
        super().__init__(parent)
        self.qview = QQuickView(parent)
        self._qml_path = qml_path
        self.ctx = ContextDict(self.qview.rootContext())
        self.ctx["appTheme"] = app_theme

        self.setLayout(ui.hbox(QWidget.createWindowContainer(self.qview, self)))

    def load_view(self):
        self.qview.setSource(str(self._qml_path))
