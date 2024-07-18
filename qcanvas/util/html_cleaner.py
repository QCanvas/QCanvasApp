import logging
import re

from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)

NBSP = "\N{NO-BREAK SPACE}"


def clean_up_html(html: str) -> str:
    html = re.sub(r"background-color:\s?initial;?", "", html)
    html = html.replace(NBSP, " ")

    doc = BeautifulSoup(html, "html.parser")

    for bad_tag in doc.find_all(["link", "script"]):
        bad_tag.decompose()

    return str(doc)
