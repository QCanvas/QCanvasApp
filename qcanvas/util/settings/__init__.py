import logging

from qcanvas.util.settings.client_settings import _ClientSettings
from qcanvas.util.settings.ui_settings import _UISettings

_logger = logging.getLogger(__name__)

client = _ClientSettings()
ui = _UISettings()
