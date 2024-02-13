from datetime import datetime

from PySide6.QtCore import QSettings


class _AppSettings:
    settings = QSettings("RetardSoft", "QCanvasViewer")

    @property
    def canvas_url(self) -> str:
        return str(self.settings.value("canvas_url"))

    @property
    def canvas_api_key(self) -> str:
        return str(self.settings.value("api_key"))