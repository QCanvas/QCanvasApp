import logging

import qcanvas.util.settings as settings
from qcanvas.util.url_checker import is_url

_logger = logging.getLogger(__name__)


def needs_setup() -> bool:
    if not settings.client.panopto_disabled and not is_url(settings.client.panopto_url):
        return True
    elif not is_url(settings.client.canvas_url):
        return True
    elif len(settings.client.canvas_api_key) == 0:
        return True
    else:
        return False
