import logging

from qcanvas.util.settings._client_settings import _ClientSettings
from qcanvas.util.settings._ui_settings import _UISettings

_logger = logging.getLogger(__name__)

client = _ClientSettings()
ui = _UISettings()
