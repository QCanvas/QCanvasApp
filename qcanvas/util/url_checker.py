import logging
from urllib.parse import urlparse

_logger = logging.getLogger(__name__)


def is_url(url: str) -> bool:
    # https://overflow.perennialte.ch/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not#
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
