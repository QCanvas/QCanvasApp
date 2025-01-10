from pathlib import Path

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget
from libqcanvas.util import remove_unwanted_whitespaces, as_local
from qasync import asyncSlot

from qcanvas.backend_connectors import FrontendResourceManager
from .qml_bridge_types import Attachment, Comment
from libqcanvas import db
import logging
from .qml_pane import QmlPane

_logger = logging.getLogger(__name__)


class CommentsPane(QmlPane):
    attachment_opened = Signal(str)

    def __init__(
        self, downloader: FrontendResourceManager, parent: QWidget | None = None
    ):
        super().__init__(Path(__file__).parent / "CommentsPane.qml", parent)
        self._downloader = downloader
        self._attachments: dict[str, db.Resource] = {}
        self._qattachments: dict[str, Attachment] = {}

        # Add context objects before we load the view
        self.ctx["comments"] = []
        self.load_view()

        self._downloader.download_finished.connect(self._download_updated)
        self._downloader.download_failed.connect(self._download_updated)

    def clear_comments(self) -> None:
        self.ctx["comments"] = []
        self._attachments.clear()
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

                self._attachments[attachment.id] = attachment
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

        self.ctx["comments"] = qcomments

    @asyncSlot(str)
    async def _on_attachment_opened(self, resource_id: str) -> None:
        if resource_id in self._attachments:
            await self._downloader.download_and_open(self._attachments[resource_id])
        else:
            _logger.warning(
                "User opened an attachment that doesn't belong to any comment! id=%s",
                resource_id,
            )

    @Slot(db.Resource)
    def _download_updated(self, resource: db.Resource) -> None:
        if resource.id in self._qattachments:
            self._qattachments[resource.id].download_state = resource.download_state
