import logging

import validators

_logger = logging.getLogger(__name__)


def is_url(url: str) -> bool:
    return validators.url(url) == True
