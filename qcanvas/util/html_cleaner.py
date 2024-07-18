import logging
import re

from bs4 import BeautifulSoup, ResultSet

_logger = logging.getLogger(__name__)


def clean_up_html(html: str) -> str:
    html = re.sub(r"background-color:\s?initial;?", "", html)
    html = html.replace("&nbsp;", " ")

    doc = BeautifulSoup(html, "html.parser")

    # Remove all scripts and css
    _remove_tags(doc.find_all(["link", "script"]))
    # Remove font awesome icons (which don't load anyway)
    _remove_tags(doc.find_all(["span"], class_=["dp-icon-content"]))

    return str(doc)


def _remove_tags(tags: ResultSet) -> None:
    for tag in tags:
        tag.decompose()
