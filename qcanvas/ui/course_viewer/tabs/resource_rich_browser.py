import html
import logging
from typing import Optional

import qcanvas_backend.database.types as db
from bs4 import BeautifulSoup, Tag
from qasync import asyncSlot
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.resources.extracting.no_extractor_error import NoExtractorError
from qcanvas_backend.util import is_link_invisible
from qtpy.QtCore import QUrl, Slot
from qtpy.QtGui import QDesktopServices
from qtpy.QtWidgets import QTextBrowser

from qcanvas.backend_connectors import FrontendResourceManager
from qcanvas.util.html_cleaner import clean_up_html
from qcanvas.util.qurl_util import file_url

_logger = logging.getLogger(__name__)


class ResourceRichBrowser(QTextBrowser):
    def __init__(self, downloader: ResourceManager):
        super().__init__()
        self._downloader = downloader
        self._content: Optional[db.CourseContentItem] = None
        self._current_content_resources: dict[str, db.Resource] = {}
        self._extractors = downloader.extractors
        self.setMinimumWidth(300)
        self.setOpenLinks(False)
        self.anchorClicked.connect(self._open_url)

        if isinstance(self._downloader, FrontendResourceManager):
            self._downloader.download_finished.connect(self._download_updated)
            self._downloader.download_failed.connect(self._download_updated)

    def show_blank(self, completely_blank: bool = False) -> None:
        if completely_blank:
            self.clear()
        else:
            self.setPlainText("No content")

        self._content = None
        self._current_content_resources.clear()

    def show_content(self, page: db.CourseContentItem) -> None:
        if page.body is None:
            self.show_blank()
        else:
            self._collect_resources(page)
            self._show_page_content(page)

    def _collect_resources(self, page: db.CourseContentItem):
        self._current_content_resources = {
            resource.id: resource for resource in page.resources
        }

    def _show_page_content(self, page: db.CourseContentItem):
        self._content = page
        html = clean_up_html(page.body)
        html = self._substitute_links(html)
        self.setHtml(html)

    def _substitute_links(self, html: str) -> str:
        doc = BeautifulSoup(html, "html.parser")

        for resource_link in doc.find_all(self._extractors.tag_whitelist):
            try:
                extractor = self._extractors.extractor_for_tag(resource_link)
                resource_id = extractor.resource_id_from_tag(resource_link)

                if is_link_invisible(resource_link):
                    _logger.debug("Found dead link for %s, removing", resource_id)
                    resource_link.decompose()
                    continue
                elif resource_id not in self._current_content_resources:
                    _logger.debug(
                        "%s not found in page resources, ignoring", resource_id
                    )
                    continue

                file_link_tag = self._create_resource_link_tag(
                    resource_id, resource_link.name == "img"
                )
                resource_link.replace_with(file_link_tag)
            except NoExtractorError:
                pass

        return str(doc)

    def _create_resource_link_tag(self, resource_id: str, is_image: bool) -> Tag:
        resource = self._current_content_resources[resource_id]

        # todo not sure if this is a good idea or not
        # if is_image and resource.download_state == db.ResourceDownloadState.DOWNLOADED:
        #     location = self._downloader.resource_download_location(resource)
        #
        #     file_link_tag = doc.new_tag(
        #         "img",
        #         attrs={
        #             "source": location.absolute(),
        #         },
        #     )
        # else:

        return BeautifulSoup(
            markup=f"""
            <a href="data:{html.escape(resource_id)}" style="font-weight: normal;">
                <img height="18" src="{html.escape(self._download_state_icon(resource.download_state))}"/>
                {html.escape(resource.file_name)}
            </a>
            """,
            features="html.parser",
        ).a

    def _download_state_icon(self, download_state: db.ResourceDownloadState) -> str:
        icon_path = ":icons/universal/downloads"
        match download_state:
            case db.ResourceDownloadState.DOWNLOADED:
                return f"{icon_path}/downloaded.svg"
            case db.ResourceDownloadState.NOT_DOWNLOADED:
                return f"{icon_path}/not_downloaded.svg"
            case db.ResourceDownloadState.FAILED:
                return f"{icon_path}/download_failed.svg"
            case _:
                raise ValueError()

    @asyncSlot(QUrl)
    async def _open_url(self, url: QUrl) -> None:
        if url.scheme() == "data":
            await self._open_resource_from_link(url)
        else:
            QDesktopServices.openUrl(url)

    async def _open_resource_from_link(self, url) -> None:
        resource_id = url.path()
        resource = self._current_content_resources[resource_id]

        try:
            await self._downloader.download(resource)
        except Exception as e:
            _logger.warning(
                "Download of resource id=%s failed", resource_id, exc_info=e
            )
            return

        resource_path = file_url(self._downloader.resource_download_location(resource))
        QDesktopServices.openUrl(resource_path)

    @Slot(db.Resource)
    def _download_updated(self, resource: db.Resource) -> None:
        if self._content is not None and resource.id in self._current_content_resources:
            # BANDAID FIX: In the following situation:
            # - Download is started
            # - Synchronisation is started
            # - Download finishes AFTER the sync
            # --> `resource` is NOT `self._current_content_resources[resource.id]`, because the sync will reload the
            # resource from the DB, but the downloader will still only know about the old resource object.
            # This causes resources not update their download state in the viewer. This line "fixes" that, but does NOT
            # address the root cause. I think reloading the resource from the DB somewhere is the only true fix for this

            if self._current_content_resources[resource.id] is not resource:
                _logger.warning(
                    "Resource has diverged from current loaded data, applying bandaid fix"
                )
                self._current_content_resources[resource.id].download_state = (
                    resource.download_state
                )

            self._show_page_content(self._content)
