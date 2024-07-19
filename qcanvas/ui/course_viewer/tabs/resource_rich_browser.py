import logging

import qcanvas_backend.database.types as db
from bs4 import BeautifulSoup
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.resources.extracting.no_extractor_error import NoExtractorError
from qcanvas_backend.net.resources.scanning.resource_scanner import ResourceScanner
from qtpy.QtWidgets import QTextBrowser

from qcanvas.util.html_cleaner import clean_up_html

_logger = logging.getLogger(__name__)


class ResourceRichBrowser(QTextBrowser):
    def __init__(self, resource_manager: ResourceManager):
        super().__init__()
        # todo use resource manager to download files when clicked!
        self._resource_manager = resource_manager
        self._extractors = resource_manager.extractors
        self.setMinimumWidth(300)

    def show_blank(self) -> None:
        self.setPlainText("No content")

    def show_page(self, page: db.CourseContentItem) -> None:
        if page.body is None:
            self.show_blank()
        else:
            html = clean_up_html(page.body)
            html = self._substitute_links(html, page.resources)
            self.setHtml(html)

    def _substitute_links(self, html: str, resources: list[db.Resource]) -> str:
        page_resources: dict[str, db.Resource] = {
            resoruce.id: resoruce for resoruce in resources
        }
        doc = BeautifulSoup(html, "html.parser")

        for resource_link in doc.find_all(self._extractors.tag_whitelist):
            try:
                # _logger.debug("Tag %s", resource_link)
                extractor = self._extractors.extractor_for_tag(resource_link)
                resource_id = extractor.resource_id_from_tag(resource_link)

                if ResourceScanner._is_link_invisible(resource_link):
                    _logger.debug("Found dead link for %s, removing", resource_id)
                    resource_link.decompose()
                    continue
                elif resource_id not in page_resources:
                    _logger.debug(
                        "%s not found in page resources, ignoring", resource_id
                    )
                    continue

                new_tag = doc.new_tag("a")
                # todo
                new_tag["href"] = f"data:,{resource_id}"
                new_tag.string = f"FILE {page_resources[resource_id].file_name}"

                resource_link.replace_with(new_tag)
            except NoExtractorError:
                pass

        return str(doc)
