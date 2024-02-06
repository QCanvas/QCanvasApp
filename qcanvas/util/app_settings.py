from datetime import datetime

from PySide6.QtCore import QSettings


class _AppSettings:
    settings = QSettings("RetardSoft", "QCanvasViewer")

    def canvas_url(self) -> str:
        return str(self.settings.value("canvas_url"))

    def canvas_api_key(self) -> str:
        return str(self.settings.value("api_key"))

    def _get_last_update(self) -> datetime:
        return self.settings.value("last_update", datetime.min)

    def _set_last_update(self, value : datetime):
        self.settings.setValue("last_update", value)

    last_update : datetime = property(
        fget=_get_last_update,
        fset=_set_last_update
    )
