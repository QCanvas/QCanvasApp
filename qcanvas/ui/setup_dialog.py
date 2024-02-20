import traceback
from threading import Semaphore
from typing import Optional

from PySide6.QtWidgets import QProgressBar
from qasync import asyncSlot

from qcanvas.QtVersionHelper.QtGui import QWindow, QDesktopServices
from qcanvas.QtVersionHelper.QtWidgets import QDialog, QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QPushButton, QDialogButtonBox, QCheckBox, QGridLayout, QMessageBox
from qcanvas.QtVersionHelper.QtCore import Qt, Slot, QUrl
from qcanvas.net.canvas import CanvasClient
from qcanvas.util import AppSettings

tutorial_url = "https://www.iorad.com/player/2053777/Canvas---How-to-generate-an-access-token-"

def row(name: str) -> QWidget:
    widget = QWidget()
    layout = QHBoxLayout()

    layout.addWidget(QLabel(name))
    layout.addWidget(QLineEdit())

    widget.setLayout(layout)

    return widget


class SetupDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None, allow_cancel: bool = True):
        super().__init__(parent)
        self.setWindowTitle("Setup")
        self._row_counter = 0
        self._operation_sem = Semaphore()

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(0)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        self.grid = QGridLayout()
        grid_widget = QWidget()
        grid_widget.setLayout(self.grid)

        stack = QVBoxLayout()

        self.canvas_url = QLineEdit(AppSettings.canvas_url or "")
        # self.panopto_url = QLineEdit()
        self.canvas_api_key = QLineEdit(AppSettings.canvas_api_key or "")

        self._row("Canvas URL", self.canvas_url)
        # self._row("Painopto URL", self.panopto_url)
        self._row("Canvas API key", self.canvas_api_key)

        self.grid.addWidget(self.progress_bar, self._row_counter, 0, 1, 2)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel if allow_cancel else QDialogButtonBox.Ok)
        button_box.addButton("How to get a canvas API key?", QDialogButtonBox.ButtonRole.HelpRole)

        button_box.helpRequested.connect(self._show_help)
        button_box.accepted.connect(self._verify)
        button_box.rejected.connect(lambda: self.reject())

        stack.addWidget(grid_widget)
        stack.addWidget(button_box)

        self.setLayout(stack)
        self.resize(500, 200)

    @asyncSlot()
    async def _verify(self):
        if self._operation_sem.acquire(False):
            try:
                def invalid(name: str):
                    msg = QMessageBox(QMessageBox.Icon.Warning,
                                      "Error",
                                      f"{name} is invalid",
                                      parent=self
                    )
                    msg.show()

                def ensure_protocol(url: str):
                    if len(url) > 0 and not (url.startswith("http://") or url.startswith("https://")):
                        return "https://" + url
                    else:
                        return url

                canvas_url_text = ensure_protocol(self.canvas_url.text().strip())
                # panopto_url_text = ensure_protocol(self.panopto_url.text().strip())
                canvas_api_key_text = self.canvas_api_key.text().strip()

                if not (len(canvas_url_text) > 0 and QUrl(canvas_url_text).isValid()):
                    invalid("Canvas URL")
                    return
                # if not (len(panopto_url_text) > 0 and QUrl(panopto_url_text).isValid()):
                #     invalid("Panopto URL")
                #     return
                elif not len(canvas_api_key_text) > 0:
                    invalid("API key")
                elif not (await self._verify_canvas_config(canvas_url_text, canvas_api_key_text)):
                    msg = QMessageBox(QMessageBox.Icon.Warning,
                                      "Error",
                                      f"The canvas URL or API key is invalid.\nPlease check you entered them correctly.",
                                      parent=self
                    )
                    msg.show()
                else:
                    AppSettings.canvas_url = canvas_url_text
                    AppSettings.canvas_api_key = canvas_api_key_text

                    self.accept()
            finally:
                self._operation_sem.release()
        else:
            QMessageBox(QMessageBox.Icon.Critical, "Error", "An operation is already in progress", parent=self).show()

    async def _verify_canvas_config(self, canvas_url: str, api_key: str) -> bool:
        self.progress_bar.show()

        try:
            return await CanvasClient.verify_config(canvas_url, api_key)
        except:
            traceback.print_exc()
            return False
        finally:
            self.progress_bar.hide()

    @Slot()
    def _show_help(self):
        msg = QMessageBox(
            QMessageBox.Icon.Information,
            "Help",
            """An interactive tutorial will open in your browser when you click OK.
            
Note that the "purpose" text doesn't matter and you can enter anything you want.

You should also leave the "expires" item blank if you want the key to last forever.

Don't share this key. You can revoke it at any time.""",
            parent=self
        )
        msg.accepted.connect(lambda: QDesktopServices.openUrl(tutorial_url))
        msg.show()


    def _row(self, name: str, widget: QWidget):
        self.grid.addWidget(QLabel(name), self._row_counter, 0)
        self.grid.addWidget(widget, self._row_counter, 1)

        self._row_counter += 1
