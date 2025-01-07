from pathlib import Path

from PySide6.QtCore import Signal, Slot
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QGroupBox, QWidget, QHBoxLayout
from libqcanvas.util import remove_unwanted_whitespaces, as_local

from qcanvas.util.layouts import layout
from .qml_bridge_types import Comment, Attachment
from qcanvas.util.auto_model import AutoModel
from qcanvas.util.context_dict import ContextDict
from libqcanvas import db


class CommentsPane(QGroupBox):
    attachment_opened = Signal(str)

    def __init__(self, parent: QWidget | None = None):
        super().__init__("Comments", parent)
        self._qview = QQuickView()
        self._ctx = ContextDict(self._qview.rootContext())
        self._comments = AutoModel[Comment](Comment, parent=self)
        # Add comments to context before we load the view
        self._ctx["comments"] = self._comments
        self._qview.setSource(str(Path(__file__).parent / "CommentsPane.qml"))
        self.setLayout(
            layout(QHBoxLayout, QWidget.createWindowContainer(self._qview, self))
        )

    def clear_comments(self) -> None:
        self._comments.clear()

    def load_comments(self, comments: list[db.SubmissionComment]) -> None:
        qcomments = []

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

            qcomments.append(
                Comment(
                    body=remove_unwanted_whitespaces(comment.body),
                    author=comment.author,
                    date=as_local(comment.creation_date).strftime("%Y-%m-%d %H:%M"),
                    attachments=AutoModel(Attachment, items=attachments),
                )
            )

        self._comments.extend(qcomments)

    @Slot()
    def _on_attachment_opened(self, resource_id: str) -> None:
        self.attachment_opened.emit(resource_id)
