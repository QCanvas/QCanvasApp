import logging
from typing import override

from PySide6.QtCore import Qt
from libqcanvas import db
from libqcanvas.net.sync.sync_receipt import SyncReceipt
from libqcanvas.util import as_local
from PySide6.QtWidgets import QLabel, QLayout, QMainWindow, QDockWidget

from qcanvas.backend_connectors import FrontendResourceManager
from qcanvas.ui.course_viewer.tabs.content_tab import ContentTab
from qcanvas.ui.course_viewer.tabs.mail_tab.mail_tree import MailTree
from qcanvas.ui.course_viewer.tabs.constants import date_strftime_format
import qcanvas.util.ui_tools as ui
from qcanvas.ui.qml_components import AttachmentsPane

_logger = logging.getLogger(__name__)


# todo maybe update has_been_read? probably not the responsibility of this class though
class MailTab(ContentTab):
    def __init__(
        self,
        *,
        course: db.Course,
        sync_receipt: SyncReceipt,
        downloader: FrontendResourceManager,
    ):
        self._main_container = QMainWindow()

        super().__init__(
            explorer=MailTree.create_from_receipt(course, sync_receipt=sync_receipt),
            title_placeholder_text="No mail selected",
            downloader=downloader,
        )

        self._main_container.setCentralWidget(self._viewer)
        self._files_pane = AttachmentsPane(downloader)
        self._files_dock = ui.dock_widget(
            widget=self._files_pane,
            title="Attachments",
            name="attachments",
            min_size=ui.size(150, 100),
            features=QDockWidget.DockWidgetFeature.DockWidgetMovable,
        )
        self._main_container.addDockWidget(
            Qt.DockWidgetArea.TopDockWidgetArea, self._files_dock
        )
        self._date_sent_label = QLabel("")
        self._sender_label = QLabel("")

        self.enable_info_grid()

    @override
    def _setup_layout(self) -> None:
        super()._setup_layout()
        self.content_grid.replaceWidget(
            self._viewer,
            self._main_container,
        )

    def setup_info_grid(self) -> QLayout:
        return ui.form_layout(
            {"From": self._sender_label, "Date": self._date_sent_label},
        )

    def update_info_grid(self, mail: db.Message) -> None:
        self._date_sent_label.setText(
            as_local(mail.creation_date).strftime(date_strftime_format)
        )
        self._sender_label.setText(mail.sender_name)

        if mail.attachments:
            self._files_pane.load_files(mail.attachments)
            self._files_dock.show()
        else:
            self._files_dock.hide()

    @override
    def _show_blank(self) -> None:
        super()._show_blank()
        self._files_dock.hide()
