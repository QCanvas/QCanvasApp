import logging
from typing import *

from qcanvas_api_clients.canvas import CanvasClientConfig
from qcanvas_api_clients.panopto import PanoptoClientConfig

from qcanvas.util import paths
from qcanvas.util.settings._mapped_setting import BoolSetting, MappedSetting

_logger = logging.getLogger(__name__)


class _ClientSettings:
    settings = paths.client_settings()
    canvas_url: MappedSetting[Optional[str]] = MappedSetting(default=None)
    canvas_api_key: MappedSetting[Optional[str]] = MappedSetting(default=None)
    panopto_url: MappedSetting[Optional[str]] = MappedSetting(default=None)
    quick_sync_enabled = BoolSetting(default=False)
    sync_on_start = BoolSetting(default=False)
    download_new_resources = BoolSetting(default=False)
    download_new_videos = BoolSetting(default=False)

    @property
    def canvas_config(self) -> CanvasClientConfig:
        return CanvasClientConfig(
            api_token=self.canvas_api_key, canvas_url=self.canvas_url
        )

    @property
    def panopto_config(self) -> PanoptoClientConfig:
        return PanoptoClientConfig(panopto_url=self.panopto_url)
