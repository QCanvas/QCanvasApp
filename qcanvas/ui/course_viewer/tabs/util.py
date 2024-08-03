from typing import Protocol

import qcanvas_backend.database.types as db
from qcanvas_backend.net.sync.sync_receipt import SyncReceipt

date_strftime_format = "%A, %Y-%m-%d, %H:%M:%S"


# todo what the hell is the point of this?
class SupportsReload(Protocol):
    def reload(self, course: db.Course, *, sync_receipt: SyncReceipt) -> None: ...
