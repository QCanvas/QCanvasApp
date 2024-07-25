import logging
from threading import Semaphore

from qasync import asyncSlot
from qcanvas_api_clients.canvas import CanvasClient, CanvasClientConfig
from qcanvas_api_clients.panopto import PanoptoClient, PanoptoClientConfig
from qcanvas_api_clients.util.request_exceptions import ConfigInvalidError
from qtpy.QtCore import QUrl, Signal, Slot
from qtpy.QtGui import QDesktopServices, QIcon
from qtpy.QtWidgets import *

import qcanvas.util.settings as settings
from qcanvas import icons
from qcanvas.util import is_url
from qcanvas.util.layouts import grid_layout_widget, layout

_logger = logging.getLogger(__name__)

_tutorial_url = (
    "https://www.iorad.com/player/2053777/Canvas---How-to-generate-an-access-token-"
)


class SetupDialog(QDialog):
    closed = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Configure QCanvas")
        self.setMinimumSize(550, 200)
        self.resize(550, 200)
        self.setWindowIcon(QIcon(icons.main_icon))

        self._semaphore = Semaphore()
        self._canvas_url_box = QLineEdit(settings.client.canvas_url)
        self._canvas_url_box.setPlaceholderText("https://instance.canvas.com")
        self._canvas_api_key_box = QLineEdit(settings.client.canvas_api_key)
        self._canvas_api_key_box.setEchoMode(QLineEdit.EchoMode.Password)
        self._panopto_url_box = QLineEdit(settings.client.panopto_url)
        self._panopto_url_box.setPlaceholderText("https://instance.panopto.com")
        self._button_box = self._setup_button_box()
        self._button_box.accepted.connect(self._accepted)
        self._button_box.helpRequested.connect(self._help_requested)
        self._waiting_indicator = self._setup_progress_bar()
        self._status_bar = QStatusBar()

        self.setLayout(
            layout(
                QVBoxLayout,
                grid_layout_widget(
                    [
                        [QLabel("Canvas URL"), self._canvas_url_box],
                        [QLabel("Canvas API Key"), self._canvas_api_key_box],
                        [QLabel("Panopto URL"), self._panopto_url_box],
                    ]
                ),
                self._waiting_indicator,
                self._button_box,
                self._status_bar,
            )
        )

    def _setup_button_box(self) -> QDialogButtonBox:
        box = QDialogButtonBox()
        box.addButton(QDialogButtonBox.StandardButton.Ok)
        box.addButton("Get a Canvas API key", QDialogButtonBox.ButtonRole.HelpRole)
        return box

    def _setup_progress_bar(self) -> QProgressBar:
        progress = QProgressBar()
        progress.setMaximum(0)
        progress.setMinimum(0)
        self._set_retain_size_when_hidden(progress)
        progress.hide()
        return progress

    def _set_retain_size_when_hidden(self, widget: QWidget) -> None:
        size_policy = widget.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        widget.setSizePolicy(size_policy)

    @asyncSlot()
    async def _accepted(self) -> None:
        if self._semaphore.acquire(False):
            try:
                self._clear_errors()

                if not self._all_inputs_valid():
                    self._status_bar.showMessage("Invalid input!", 5000)
                    return

                self._waiting_indicator.setVisible(True)
                self._status_bar.showMessage("Checking configuration...")

                canvas_config = CanvasClientConfig(
                    api_token=self._canvas_api_key_box.text().strip(),
                    canvas_url=self._get_url(self._canvas_url_box),
                )

                if not await self._check_canvas_config(canvas_config):
                    return

                if not await self._check_panopto_config(canvas_config):
                    self._show_panopto_help()
                    return
            except Exception as e:
                self._status_bar.showMessage(f"An error occurred: {e}", 5000)
                _logger.warning("Checking config failed", exc_info=e)
            finally:
                self._waiting_indicator.setVisible(False)
                self._semaphore.release()

            _logger.debug("Credentials are a-ok!")
            self._save_and_close()
        else:
            _logger.debug("Validation already in progress")

    def _clear_errors(self) -> None:
        for line_edit in [
            self._canvas_url_box,
            self._panopto_url_box,
            self._canvas_api_key_box,
        ]:
            self._status_bar.clearMessage()
            line_edit.setStyleSheet(None)
            line_edit.setToolTip(None)

    def _all_inputs_valid(self) -> bool:
        all_valid = True

        if not is_url(self._get_url(self._canvas_url_box)):
            all_valid = False
            self._show_error(self._canvas_url_box, "Canvas URL is invalid")
        if len(self._canvas_api_key_box.text().strip()) == 0:
            all_valid = False
            self._show_error(self._canvas_api_key_box, "Canvas API key is empty")
        if not is_url(self._get_url(self._panopto_url_box)):
            all_valid = False
            self._show_error(self._panopto_url_box, "Panopto URL is invalid")

        return all_valid

    def _get_url(self, line_edit: QLineEdit) -> str:
        url = line_edit.text().strip()

        if not url.startswith("http"):
            return "https://" + url
        else:
            return url

    async def _check_canvas_config(self, canvas_config: CanvasClientConfig) -> bool:
        try:
            await CanvasClient.verify_config(canvas_config)
            return True
        except ConfigInvalidError:
            self._show_error(self._canvas_api_key_box, "Canvas API key is invalid")
            return False

    def _show_error(self, line_edit: QLineEdit, text: str) -> None:
        line_edit.setToolTip(text)
        self._waiting_indicator.hide()
        self._highlight_line_edit(line_edit)

    def _highlight_line_edit(self, line_edit: QLineEdit) -> None:
        line_edit.setStyleSheet("QLineEdit { border: 1px solid red }")

    async def _check_panopto_config(self, canvas_config: CanvasClientConfig) -> bool:
        client = CanvasClient(canvas_config)
        try:
            await PanoptoClient.verify_config(
                PanoptoClientConfig(panopto_url=self._get_url(self._panopto_url_box)),
                client,
            )
            return True
        except ConfigInvalidError:
            return False
        finally:
            await client.aclose()

    def _show_panopto_help(self):
        msg = QMessageBox(
            QMessageBox.Icon.Information,
            "Panopto Authentication",
            "In order for QCanvas to use Panopto, you need to link your Panopto account to your Canvas account. "
            "A page will open in your web browser to do this when you click OK. It may ask you to sign into Canvas.\n\n"
            'Please tick "Remember my authorisation for this service" or QCanvas may not function correctly.\n\n'
            "QCanvas can't access anything entered in your browser.",
            QMessageBox.StandardButton.Ok,
            self,
        )
        msg.accepted.connect(self._open_panopto_login)
        msg.show()

    @Slot()
    def _open_panopto_login(self) -> None:
        url = QUrl(self._get_url(self._panopto_url_box))
        url.setPath("/Panopto/Pages/Auth/Login.aspx")
        url.setQuery("instance=Canvas&AllowBounce=true")
        QDesktopServices.openUrl(url)

    def _save_and_close(self) -> None:
        settings.client.canvas_url = self._get_url(self._canvas_url_box)
        settings.client.panopto_url = self._get_url(self._panopto_url_box)
        settings.client.canvas_api_key = self._canvas_api_key_box.text().strip()
        self.closed.emit()
        self.close()

    @Slot()
    def _help_requested(self) -> None:
        msg = QMessageBox(
            QMessageBox.Icon.Information,
            "Help",
            "An interactive tutorial will open in your browser when you click OK.\n\n"
            'Note that the "purpose" text doesn\'t matter and you can enter anything you want.\n\n'
            'You should also leave the "expires" item blank if you want the key to last forever.\n\n'
            "Don't share this key. You can revoke it at any time.",
            parent=self,
        )
        msg.accepted.connect(self._open_tutorial)
        msg.show()

    @Slot()
    def _open_tutorial(self) -> None:
        QDesktopServices.openUrl(QUrl(_tutorial_url))
