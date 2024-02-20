from qcanvas.QtVersionHelper.QtCore import QSettings, QUrl


class _AppSettings:
    def __init__(self):
        self.settings = QSettings("QCanvas", "client")
        self.auxiliary = QSettings("QCanvas", "ui")
        self._canvas_url = self.settings.value("canvas_url", None)
        self._api_key = self.settings.value("api_key", defaultValue=None)

    @property
    def canvas_url(self) -> str | None:
        return self._canvas_url

    @canvas_url.setter
    def canvas_url(self, value: str):
        self._canvas_url = value
        self.settings.setValue("canvas_url", value)

    @property
    def canvas_api_key(self) -> str | None:
        return self._api_key

    @canvas_api_key.setter
    def canvas_api_key(self, value: str):
        self._api_key = value
        self.settings.setValue("api_key", value)

    @property
    def is_set(self):
        return self.canvas_url is not None and QUrl(self.canvas_url).isValid() and self.canvas_url is not None


