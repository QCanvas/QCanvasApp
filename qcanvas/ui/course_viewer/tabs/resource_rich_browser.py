import logging
from typing import Optional

import qcanvas_backend.database.types as db
from bs4 import BeautifulSoup, Tag
from qasync import asyncSlot
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager
from qcanvas_backend.net.resources.extracting.no_extractor_error import NoExtractorError
from qcanvas_backend.net.resources.scanning.resource_scanner import ResourceScanner
from qtpy.QtCore import QUrl, Slot
from qtpy.QtGui import QDesktopServices
from qtpy.QtWidgets import QTextBrowser

from qcanvas import icons
from qcanvas.backend_connectors import FrontendResourceManager
from qcanvas.util.html_cleaner import clean_up_html
from qcanvas.util.qurl_util import file_url

_logger = logging.getLogger(__name__)


# class _DarkListener(QObject):
#     theme_changed = Signal(str)
#
#     def __init__(self):
#         super().__init__()
#
#         self._thread = threading.Thread(target=darkdetect.listener, args=(self._emit,))
#         self._thread.daemon = True
#         self._thread.start()
#
#     def _emit(self, theme: str) -> None:
#         self.theme_changed.emit(theme)
#
# _dark_listener = _DarkListener()


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

        # _dark_listener.theme_changed.connect(self._theme_changed)

    # @Slot()
    # def _theme_changed(self, theme: str) -> None:
    #     print(theme)

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

                # FIXME private method
                if ResourceScanner._is_link_invisible(resource_link):
                    _logger.debug("Found dead link for %s, removing", resource_id)
                    resource_link.decompose()
                    continue
                elif resource_id not in self._current_content_resources:
                    _logger.debug(
                        "%s not found in page resources, ignoring", resource_id
                    )
                    continue

                file_link_tag = self._create_resource_link_tag(doc, resource_id)
                resource_link.replace_with(file_link_tag)
            except NoExtractorError:
                pass

        return str(doc)

    def _create_resource_link_tag(self, doc: BeautifulSoup, resource_id: str) -> Tag:
        resource = self._current_content_resources[resource_id]

        file_link_tag = doc.new_tag(
            "a",
            attrs={
                "href": f"data:{resource_id}",
            },
        )

        file_link_tag.append(self._file_icon_tag(doc, resource.download_state))
        file_link_tag.append("\N{NO-BREAK SPACE}" + resource.file_name)

        _logger.debug(str(file_link_tag))

        return file_link_tag

    def _file_icon_tag(
        self, document: BeautifulSoup, download_state: db.ResourceDownloadState
    ) -> Tag:
        return document.new_tag(
            "img",
            attrs={
                "src": self._download_state_icon(download_state),
                "style": "vertical-align:middle",
                "width": 18,
            },
        )

    def _download_state_icon(self, download_state: db.ResourceDownloadState) -> str:
        match download_state:
            case db.ResourceDownloadState.DOWNLOADED:
                return icons.file_downloaded
            case db.ResourceDownloadState.NOT_DOWNLOADED:
                return icons.file_not_downloaded
            case db.ResourceDownloadState.FAILED:
                return icons.file_download_failed
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
            self._show_page_content(self._content)
