from qcanvas.QtVersionHelper.QtCore import QSettings, QUrl


class _AppSettings:
    settings = QSettings("RetardSoft", "QCanvasViewer")

    @property
    def canvas_url(self) -> str | None:
        return self.settings.value("canvas_url", None)

    @canvas_url.setter
    def canvas_url(self, value: str):
        self.settings.setValue("canvas_url", value)

    @property
    def canvas_api_key(self) -> str | None:
        return self.settings.value("api_key", defaultValue=None)

    @canvas_api_key.setter
    def canvas_api_key(self, value: str):
        self.settings.setValue("api_key", value)

    @property
    def is_set(self):
        return self.canvas_url is not None and QUrl(self.canvas_url).isValid() and self.canvas_url is not None


