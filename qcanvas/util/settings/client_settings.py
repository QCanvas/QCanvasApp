import logging
from typing import *

from qcanvas_api_clients.canvas import CanvasClientConfig
from qcanvas_api_clients.panopto import PanoptoClientConfig

from qcanvas.util import paths
from qcanvas.util.settings.mapped_setting import MappedSetting

_logger = logging.getLogger(__name__)


class _ClientSettings:
    settings = paths.client_settings()
    canvas_url: MappedSetting[Optional[str]] = MappedSetting(default=None)
    canvas_api_key: MappedSetting[Optional[str]] = MappedSetting(default=None)
    panopto_url: MappedSetting[Optional[str]] = MappedSetting(default=None)

    @property
    def canvas_config(self) -> CanvasClientConfig:
        return CanvasClientConfig(
            api_token=self.canvas_api_key, canvas_url=self.canvas_url
        )

    @property
    def panopto_config(self) -> PanoptoClientConfig:
        return PanoptoClientConfig(panopto_url=self.panopto_url)
