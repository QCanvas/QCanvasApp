import traceback
from threading import Semaphore
from typing import Optional

from PySide6.QtCore import Slot, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, \
    QDialogButtonBox, QGridLayout, QMessageBox
from PySide6.QtWidgets import QProgressBar
from qasync import asyncSlot

from qcanvas.net.canvas import CanvasClient
from qcanvas.util.app_settings import settings

tutorial_url = "https://www.iorad.com/player/2053777/Canvas---How-to-generate-an-access-token-"


def row(name: str) -> QWidget:
    widget = QWidget()
    layout = QHBoxLayout()

    layout.addWidget(QLabel(name))
    layout.addWidget(QLineEdit())

    widget.setLayout(layout)

    return widget


class SetupDialog(QDialog):
    """
    The dialog shown to the user when the canvas api key/url is invalid, such as the first time the user is opening the application.
    The dialog asks for an api key and canvas url then verifies them before saving them to the primary app settings file.
    """
    def __init__(self, parent: Optional[QWidget] = None, allow_cancel: bool = True):
        super().__init__(parent)

        self.setWindowTitle("Setup")
        self._row_counter = 0
        self._operation_sem = Semaphore()
        self.allow_cancel = allow_cancel

        # Progress bar used to indicate that an operation is underway and the application has not frozen
        self.operation_activity_indicator = QProgressBar()
        self.operation_activity_indicator.setMaximum(0)
        self.operation_activity_indicator.setMinimum(0)
        self.operation_activity_indicator.setValue(0)
        self.operation_activity_indicator.hide()

        self.grid = QGridLayout()

        # Line edits for the different properties
        self.canvas_url = QLineEdit(settings.canvas_url or "")
        self.panopto_url = QLineEdit()
        self.canvas_api_key = QLineEdit(settings.api_key or "")

        # Add the line edits to the dialog
        self._row("Canvas URL", self.canvas_url)
        self._row("Painopto URL", self.panopto_url)
        self._row("Canvas API key", self.canvas_api_key)

        # Add the activity indicator to the dialog
        self.grid.addWidget(self.operation_activity_indicator, self._row_counter, 0, 1, 2)

        # Setup the rest of the layout
        grid_widget = QWidget()
        grid_widget.setLayout(self.grid)

        stack = QVBoxLayout()
        stack.addWidget(grid_widget)
        stack.addWidget(self._setup_button_box())

        self.setLayout(stack)
        self.resize(500, 200)

    def _setup_button_box(self) -> QDialogButtonBox:
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel if self.allow_cancel else QDialogButtonBox.StandardButton.Save)
        # Add a help button to show the user how to get a canvas api key
        button_box.addButton("How to get a canvas API key?", QDialogButtonBox.ButtonRole.HelpRole)
        # Connect signals
        button_box.helpRequested.connect(self._show_help)
        button_box.accepted.connect(self._verify)
        button_box.rejected.connect(lambda: self.reject())

        return button_box

    @asyncSlot()
    async def _verify(self) -> None:
        """
        Verifies the user's inputs before saving them
        """
        if self._operation_sem.acquire(False):
            try:
                canvas_url_text = self.ensure_protocol(self.canvas_url.text().strip())
                panopto_url_text = self.ensure_protocol(self.panopto_url.text().strip())
                canvas_api_key_text = self.canvas_api_key.text().strip()

                if not (len(canvas_url_text) > 0 and QUrl(canvas_url_text).isValid()):
                    self._show_invalid_msgbox("Canvas URL")
                    return
                if not (len(panopto_url_text) > 0 and QUrl(panopto_url_text).isValid()):
                    self._show_invalid_msgbox("Panopto URL")
                    return
                elif not len(canvas_api_key_text) > 0:
                    self._show_invalid_msgbox("API key")
                elif not (await self._verify_canvas_config(canvas_url_text, canvas_api_key_text)):
                    # Show message box saying that either the url or api key is incorrect
                    QMessageBox(
                        QMessageBox.Icon.Critical,
                        "Error",
                        f"The canvas URL or API key is invalid.\nPlease check you entered them correctly.",
                        parent=self
                    ).show()
                else:
                    # If nothing was wrong, everything should be fine
                    # Save the url and api key
                    settings.canvas_url = canvas_url_text
                    settings.panopto_url = panopto_url_text
                    settings.api_key = canvas_api_key_text

                    self.accept()
            finally:
                self._operation_sem.release()
        else:
            QMessageBox(QMessageBox.Icon.Critical, "Error", "An operation is already in progress", parent=self).show()

    def _show_invalid_msgbox(self, field_name: str) -> None:
        """
        Shows a message box saying that that specified field is invalid
        """
        QMessageBox(
            QMessageBox.Icon.Critical,
            "Error",
            f"{field_name} is invalid",
            parent=self
        ).show()

    @staticmethod
    def ensure_protocol(url: str) -> str:
        # Check if the url is blank/empty so we can tell if the user didn't input anything
        if len(url) > 0 and not (url.startswith("http://") or url.startswith("https://")):
            return "https://" + url
        else:
            return url

    async def _verify_canvas_config(self, canvas_url: str, api_key: str) -> bool:
        """
        Makes a network request to canvas to ensure the provided url and api key are correct

        Returns
        -------
        bool
            True if valid, False if invalid
        """
        self.operation_activity_indicator.show()

        try:
            return await CanvasClient.verify_config(canvas_url, api_key)
        except:
            traceback.print_exc()
            return False
        finally:
            self.operation_activity_indicator.hide()

    @Slot()
    def _show_help(self) -> None:
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

    def _row(self, name: str, widget: QWidget) -> None:
        """
        Shortcut to add a field with a label to the dialog
        """
        self.grid.addWidget(QLabel(name), self._row_counter, 0)
        self.grid.addWidget(widget, self._row_counter, 1)

        self._row_counter += 1
