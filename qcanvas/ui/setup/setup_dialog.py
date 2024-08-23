import logging
from threading import Semaphore
from typing import Optional

from qasync import asyncSlot
from qcanvas_api_clients.canvas import CanvasClient, CanvasClientConfig
from qcanvas_api_clients.panopto import PanoptoClient, PanoptoClientConfig
from qcanvas_api_clients.util.request_exceptions import ConfigInvalidError
from qtpy.QtCore import Qt, QUrl, Signal, Slot
from qtpy.QtGui import QDesktopServices, QIcon
from qtpy.QtWidgets import *

import qcanvas.util.settings as settings
from qcanvas import icons
from qcanvas.util.layouts import GridItem, grid_layout_widget, layout
from qcanvas.util.url_checker import is_url

_logger = logging.getLogger(__name__)

_tutorial_url = (
    "https://www.iorad.com/player/2053777/Canvas---How-to-generate-an-access-token-"
)


class _InputRow:
    def __init__(
        self,
        *,
        label: str,
        initial_value: str,
        placeholder_text: Optional[str] = None,
        is_password: bool = False,
    ):
        self._label = QLabel(label)
        self._input = QLineEdit(initial_value)

        if placeholder_text is not None:
            self._input.setPlaceholderText(placeholder_text)

        if is_password:
            self._input.setEchoMode(QLineEdit.EchoMode.Password)

    def set_error(self, message: Optional[str]) -> None:
        self._input.setStyleSheet("QLineEdit { border: 1px solid red }")
        self._input.setToolTip(message)

    def clear_error(self) -> None:
        self._input.setStyleSheet(None)
        self._input.setToolTip(None)

    def grid_row(self) -> list[QWidget]:
        return [self._label, self._input]

    def disable(self) -> None:
        self._input.setEnabled(False)

    @property
    def enabled(self) -> bool:
        return self._input.isEnabled()

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._input.setEnabled(value)

    @property
    def text(self) -> str:
        return self._input.text().strip()

    @property
    def url_text(self) -> str:
        url = self.text

        if not url.startswith("http"):
            return "https://" + url
        else:
            return url

    @property
    def is_valid_url(self) -> bool:
        return is_url(self.url_text)

    @property
    def is_empty(self) -> bool:
        return len(self.text) == 0


class SetupDialog(QDialog):
    closed = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Configure QCanvas")
        self.setMinimumSize(550, 200)
        self.resize(550, 200)
        self.setWindowIcon(QIcon(icons.branding.main_icon))

        self._semaphore = Semaphore()

        self._canvas_url_box = _InputRow(
            label="Canvas URL",
            initial_value=settings.client.canvas_url,
            placeholder_text="https://instance.canvas.com",
        )
        self._panopto_url_box = _InputRow(
            label="Panopto URL",
            initial_value=settings.client.panopto_url,
            placeholder_text="https://instance.panopto.com",
        )
        self._canvas_api_key_box = _InputRow(
            label="Canvas API Key",
            initial_value=settings.client.canvas_api_key,
            is_password=True,
        )
        self._disable_panopto_checkbox = QCheckBox("Continue without Panopto")
        self._disable_panopto_checkbox.checkStateChanged.connect(
            self._disable_panopto_check_changed
        )
        self._button_box = self._setup_button_box()
        self._waiting_indicator = self._setup_progress_bar()

        self.setLayout(
            layout(
                QVBoxLayout,
                grid_layout_widget(
                    [
                        self._canvas_url_box.grid_row(),
                        self._canvas_api_key_box.grid_row(),
                        self._panopto_url_box.grid_row(),
                        [
                            GridItem(
                                self._disable_panopto_checkbox,
                                col_span=2,
                                alignment=Qt.AlignmentFlag.AlignRight,
                            )
                        ],
                    ]
                ),
                self._waiting_indicator,
                self._button_box,
            )
        )

    def _setup_button_box(self) -> QDialogButtonBox:
        box = QDialogButtonBox()
        box.addButton(QDialogButtonBox.StandardButton.Ok)
        box.addButton("Get a Canvas API Key", QDialogButtonBox.ButtonRole.HelpRole)

        box.accepted.connect(self._verify_settings)
        box.helpRequested.connect(self._help_requested)
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
    async def _verify_settings(self) -> None:
        if self._semaphore.acquire(False):
            try:
                self._clear_errors()

                if not self._check_all_inputs():
                    return

                self._waiting_indicator.setVisible(True)

                canvas_config = CanvasClientConfig(
                    api_token=self._canvas_api_key_box.text,
                    canvas_url=self._canvas_url_box.url_text,
                )

                if not await self._check_canvas_config(canvas_config):
                    return

                if self._panopto_enabled:
                    if not await self._check_panopto_config(canvas_config):
                        self._show_panopto_help()
                        return
            except Exception as e:
                _logger.warning("Checking config failed", exc_info=e)

                error_box = QErrorMessage(self)
                error_box.showMessage(f"Checking config failed: {e}")
            finally:
                self._waiting_indicator.setVisible(False)
                self._semaphore.release()

            _logger.debug("Credentials are a-ok!")
            self._save_and_close()
        else:
            _logger.debug("Validation already in progress")

    def _clear_errors(self) -> None:
        self._canvas_url_box.clear_error()
        self._panopto_url_box.clear_error()
        self._canvas_api_key_box.clear_error()

    def _check_all_inputs(self) -> bool:
        all_valid = True

        if not self._canvas_url_box.is_valid_url:
            all_valid = False
            self._canvas_url_box.set_error("Canvas URL is invalid")

        if self._canvas_api_key_box.is_empty:
            all_valid = False
            self._canvas_api_key_box.set_error("Canvas API key is empty")

        if self._panopto_enabled and not self._panopto_url_box.is_valid_url:
            all_valid = False
            self._panopto_url_box.set_error("Panopto URL is invalid")

        return all_valid

    async def _check_canvas_config(self, canvas_config: CanvasClientConfig) -> bool:
        try:
            await CanvasClient.verify_config(canvas_config)
            return True
        except ConfigInvalidError:
            self._canvas_api_key_box.set_error("Canvas API key is invalid")
            return False

    async def _check_panopto_config(self, canvas_config: CanvasClientConfig) -> bool:
        client = CanvasClient(canvas_config)
        try:
            await PanoptoClient.verify_config(
                PanoptoClientConfig(panopto_url=self._panopto_url_box.url_text),
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
        url = QUrl(self._panopto_url_box.url_text)
        url.setPath("/Panopto/Pages/Auth/Login.aspx")
        url.setQuery("instance=Canvas&AllowBounce=true")
        QDesktopServices.openUrl(url)

    def _save_and_close(self) -> None:
        settings.client.canvas_url = self._canvas_url_box.url_text

        if self._panopto_enabled:
            settings.client.panopto_url = self._panopto_url_box.url_text
        else:
            settings.client.panopto_disabled = True

        settings.client.canvas_api_key = self._canvas_api_key_box.text

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

    @Slot(Qt.CheckState)
    def _disable_panopto_check_changed(self, state: Qt.CheckState) -> None:
        self._panopto_url_box.enabled = state == Qt.CheckState.Unchecked

    @property
    def _panopto_enabled(self) -> bool:
        return self._disable_panopto_checkbox.checkState() == Qt.CheckState.Unchecked
