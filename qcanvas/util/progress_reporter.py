import itertools
from abc import ABC, abstractmethod
from typing import Any


class ProgressSection:
    """
    Convenience class for reporting on a section of a larger task
    """

    def __init__(self, section_name: str, total_progress: int, reporter: "ProgressReporter"):
        self.total_progress = total_progress
        self.reporter = reporter
        self._counter = itertools.count(1)  # Start at 1 instead of 0
        self.reporter.section_started(section_name, total_progress)

    def increment_progress(self, *args):
        self.reporter.progress(next(self._counter), self.total_progress)


class ProgressReporter(ABC):
    """
    A progress reporter is passed to a function which then uses it to report the progress for whatever task it performs to another place.
    Only 1 section should be active at a time.
    """

    @abstractmethod
    def section_started(self, section_name: str, total_progress: int) -> None:
        """
        Signals that a new section of a task has started
        Parameters
        ----------
        section_name
            The name of the new task section
        """
        ...

    @abstractmethod
    def progress(self, current_progress: int, total_progress: int) -> None:
        """
        Updates the current progress of the current task
        Parameters
        ----------
        current_progress
            The current amount of progress, e.g. the number of bytes of a file that have been downloaded
        total_progress
            The total or final amount of progress, e.g. the size of a download
        """
        ...

    @abstractmethod
    def finished(self) -> None:
        """
        Signals that the task is finished and there is nothing left to do
        """
        ...

    @abstractmethod
    def errored(self, context: Any) -> None:
        """
        Signals that the task could not be completed
        Parameters
        ----------
        context
            Any information about why the task failed
        """
        ...

    def section(self, section_name: str, total_progress: int) -> ProgressSection:
        """
        Creates a ProgressSection for this reporter, for reporting on a section of a larger task
        Parameters
        ----------
        section_name
            The name of the section
        total_progress
            The total or final amount of progress, e.g. the size of a download
        Returns
        -------
        ProgressSection
            The created section
        """
        return ProgressSection(section_name, total_progress, self)


class _NoopReporter(ProgressReporter):

    def section_started(self, section_name: str, total_progress: int) -> None:
        pass

    def progress(self, current_progress: int, total: int) -> None:
        pass

    def finished(self) -> None:
        pass

    def errored(self, context: Any) -> None:
        pass


noop_reporter = _NoopReporter()
