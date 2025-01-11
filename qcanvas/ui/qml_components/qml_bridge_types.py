from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import ListProperty, QmlElement
from libqcanvas.database.tables import ResourceDownloadState


QML_IMPORT_NAME = "QCanvas"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Attachment(QObject):
    file_name_changed = Signal()
    resource_id_changed = Signal()
    download_state_changed = Signal()

    # Emitted by AttachmentsListDelegate when the user clicks on an attachment
    opened = Signal(str)

    def __init__(
        self,
        file_name: str,
        resource_id: str,
        download_state: ResourceDownloadState,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._file_name = file_name
        self._resource_id = resource_id
        self._download_state = download_state.name

    @Property(str, notify=file_name_changed)
    def file_name(self) -> str:
        return self._file_name

    @Property(str, notify=resource_id_changed)
    def resource_id(self) -> str:
        return self._resource_id

    @Property(str, notify=download_state_changed)
    def download_state(self) -> str:
        return self._download_state

    @download_state.setter
    def download_state(self, value: ResourceDownloadState):
        if value.name != self._download_state:
            self._download_state = value.name
            self.download_state_changed.emit()


@QmlElement
class Comment(QObject):
    body_changed = Signal()
    author_changed = Signal()
    date_changed = Signal()
    attachments_changed = Signal()

    def __init__(
        self,
        body: str,
        author: str,
        date: str,
        attachments: list[Attachment],
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self._body = body
        self._author = author
        self._date = date
        self._attachments = attachments

    @Property(str, notify=body_changed)
    def body(self) -> str:
        return self._body

    @Property(str, notify=date_changed)
    def date(self) -> str:
        return self._date

    @Property(str, notify=author_changed)
    def author(self) -> str:
        return self._author

    def attachment(self, n) -> Attachment:
        return self._attachments[n]

    def attachment_count(self) -> int:
        return len(self._attachments)

    # You must set `count`, `at` and `notify` EXPLICTLY (even if you name them according to the examples, which examples are all inconsistent and wrong).
    # Qt?? Are you ok???
    # Oh and you have to use `.length` instead of `.count` on the QML side because javascript.
    attachments = ListProperty(
        Attachment, count=attachment_count, at=attachment, notify=attachments_changed
    )
