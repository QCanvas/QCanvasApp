from dataclasses import dataclass

from PySide6.QtCore import Property, QObject, Signal
from libqcanvas.database.tables import ResourceDownloadState


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


@dataclass
class Comment:
    body: str
    author: str
    date: str
    attachments: object
