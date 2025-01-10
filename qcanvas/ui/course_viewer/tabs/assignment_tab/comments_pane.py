from pathlib import Path

from PySide6.QtCore import Signal, Slot
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QGroupBox, QWidget, QHBoxLayout
from libqcanvas.util import remove_unwanted_whitespaces, as_local
from qasync import asyncSlot

from qcanvas.backend_connectors import FrontendResourceManager
from qcanvas.util.layouts import layout
from .qml_bridge_types import Attachment, Comment
from qcanvas.util.context_dict import ContextDict
from libqcanvas import db
import logging
from qcanvas.theme import app_theme

_logger = logging.getLogger(__name__)


class CommentsPane(QGroupBox):
    attachment_opened = Signal(str)

    def __init__(
        self, downloader: FrontendResourceManager, parent: QWidget | None = None
    ):
        super().__init__(parent)
        self._downloader = downloader
        self._resources: dict[str, db.Resource] = {}
        self._qattachments: dict[str, Attachment] = {}

        self._qview = QQuickView()
        self._ctx = ContextDict(self._qview.rootContext())
        # Add context objects before we load the view
        self._ctx["comments"] = []
        self._ctx["appTheme"] = app_theme

        self._qview.setSource(str(Path(__file__).parent / "CommentsPane.qml"))
        self.setLayout(
            layout(QHBoxLayout, QWidget.createWindowContainer(self._qview, self))
        )

        self._downloader.download_finished.connect(self._download_updated)
        self._downloader.download_failed.connect(self._download_updated)

    def clear_comments(self) -> None:
        self._resources.clear()
        self._qattachments.clear()

    def load_comments(self, comments: list[db.SubmissionComment]) -> None:
        qcomments = []

        self.parent().setWindowTitle(f"Comments ({len(comments)})")

        for comment in comments:
            attachments = []

            for attachment in comment.attachments:
                qattachment = Attachment(
                    file_name=attachment.file_name,
                    resource_id=attachment.id,
                    download_state=attachment.download_state,
                )
                qattachment.opened.connect(self._on_attachment_opened)
                attachments.append(qattachment)

                self._resources[attachment.id] = attachment
                self._qattachments[attachment.id] = qattachment

            qcomments.append(
                Comment(
                    body=remove_unwanted_whitespaces(comment.body),
                    author=comment.author,
                    date=as_local(comment.creation_date).strftime("%Y-%m-%d %H:%M"),
                    attachments=attachments,
                    parent=self,
                )
            )

        self._ctx["comments"] = qcomments

    @asyncSlot(str)
    async def _on_attachment_opened(self, resource_id: str) -> None:
        if resource_id in self._resources:
            await self._downloader.download_and_open(self._resources[resource_id])
        else:
            _logger.warning(
                "User opened an attachment that doesn't belong to any comment! id=%s",
                resource_id,
            )

    @Slot(db.Resource)
    def _download_updated(self, resource: db.Resource) -> None:
        if resource.id in self._qattachments:
            self._qattachments[resource.id].download_state = resource.download_state
