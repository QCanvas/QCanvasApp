from typing import Any

from PySide6.QtWidgets import QStatusBar, QProgressBar

from qcanvas.util.progress_reporter import ProgressReporter


class StatusBarReporter(ProgressReporter):
    def __init__(self, status_bar: QStatusBar):
        self.status_bar = status_bar
        self.section_name: None | str = None
        self.progress_bar: QProgressBar | None = None

    def section_started(self, section_name: str, total_progress: int) -> None:
        self.section_name = section_name
        self.status_bar.showMessage(section_name)

        if self.progress_bar is None:
            self.progress_bar = QProgressBar(self.status_bar)
            self.progress_bar.setMaximumHeight(self.status_bar.height())
            self.progress_bar.setMinimum(0)
            self.status_bar.addPermanentWidget(self.progress_bar)

        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(total_progress)

    def progress(self, current_progress: int, total: int) -> None:
        if self.progress_bar is not None:
            self.progress_bar.setValue(current_progress)

    def finished(self) -> None:
        self.status_bar.removeWidget(self.progress_bar)
        self.progress_bar = None
        self.status_bar.showMessage("Finished", 5000)

    def errored(self, context: Any) -> None:
        if self.status_bar.parent() is not None:
            self.status_bar.removeWidget(self.progress_bar)
            self.progress_bar = None
            self.status_bar.showMessage("Synchronisation error!!", 5000)
