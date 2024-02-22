import qdarktheme

from qcanvas.QtVersionHelper.QtCore import QSettings, QUrl


def ensure_theme_is_valid(theme: str) -> str:
    if theme not in ["auto", "light", "dark", "native"]:
        return "light"
    else:
        return theme


class _AppSettings:
    def __init__(self):
        self.settings = QSettings("QCanvas", "client")
        self.auxiliary = QSettings("QCanvas", "ui")
        self._canvas_url = self.settings.value("canvas_url", None)
        self._api_key = self.settings.value("api_key", defaultValue=None)
        self._ignored_update = self.settings.value("ignored_update", defaultValue=None)
        self._theme = ensure_theme_is_valid(self.settings.value("theme", defaultValue="light"))

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
    def last_ignored_update(self) -> str | None:
        return self._ignored_update

    @last_ignored_update.setter
    def last_ignored_update(self, value: str):
        self._ignored_update = value
        self.settings.setValue("ignored_update", value)

    @property
    def theme(self) -> str | None:
        return self._theme

    @theme.setter
    def theme(self, value: str):
        value = ensure_theme_is_valid(value)
        self._theme = value
        self.settings.setValue("theme", value)

    # fixme should this really be here
    def apply_selected_theme(self):
        if self.theme != "native":
            qdarktheme.setup_theme(
                self.theme,
                custom_colors={"primary": "FF804F"}
            )

    @property
    def is_set(self):
        return self.canvas_url is not None and QUrl(self.canvas_url).isValid() and self.canvas_url is not None
