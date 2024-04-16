from PySide6.QtWidgets import QTreeWidgetItem

from qcanvas.db import database as db
from qcanvas.util.helpers import file_icon_helper


class FileRow(QTreeWidgetItem):
    def __init__(self, resource: db.Resource):
        # Set column names
        super().__init__(
            [
                resource.file_name,
                resource.date_discovered.strftime("%Y-%m-%d"),
                self.sizeof_fmt(resource.file_size),
            ]
        )

        # Set the icon for this file, displayed in the name column
        self.setIcon(0, file_icon_helper.icon_for_filename(resource.file_name))

        self.resource = resource
        # This is used to pass the download progress value from download_progress_updated to FileColumnDelegate. This way
        # it means we don't have to get the download progress from the DownloadPool a second time with an async function
        # (which is undesirable from an item delegate...). Use -1 to show that the file is not currently downloading.
        self.download_progres = -1

    # https://code.whatever.social/questions/1094841/get-human-readable-version-of-file-size#1094933
    @staticmethod
    def sizeof_fmt(num, suffix="B"):
        for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"
