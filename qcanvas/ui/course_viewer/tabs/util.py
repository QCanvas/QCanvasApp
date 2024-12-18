from typing import Protocol

from libqcanvas import db
from libqcanvas.net.sync.sync_receipt import SyncReceipt

date_strftime_format = "%A, %Y-%m-%d, %H:%M:%S"


# todo what the hell is the point of this?
class SupportsReload(Protocol):
    def reload(self, course: db.Course, *, sync_receipt: SyncReceipt) -> None: ...
