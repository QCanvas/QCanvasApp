import asyncio
import logging

from PySide6.QtCore import Qt
from libqcanvas import db
from libqcanvas.net.resources.download.resource_manager import ResourceManager
from libqcanvas.net.sync.sync_receipt import SyncReceipt
from PySide6.QtWidgets import QMessageBox, QWidget

import qcanvas.settings as settings

_logger = logging.getLogger(__name__)


async def download_new_resources(
    *,
    all_resources: dict[str, db.Resource],
    receipt: SyncReceipt,
    downloader: ResourceManager,
    parent_window: QWidget,
) -> None:
    resources_to_download = []

    for file_id in receipt.updates[db.Resource]:
        resource = all_resources[file_id]

        if _should_auto_download_resource(resource, resource_manager=downloader):
            resources_to_download.append(resource)

    resource_count = len(resources_to_download)

    if resource_count == 0:
        return
    elif resource_count > 20:
        msg = _confirmation_messagebox(resource_count, parent_window)
        msg.show()
        msg.accepted.connect(
            lambda: asyncio.get_running_loop().create_task(
                downloader.batch_download(resources_to_download),
            ),
            Qt.ConnectionType.SingleShotConnection,
        )
    else:
        await downloader.batch_download(resources_to_download)


def _should_auto_download_resource(
    resource: db.Resource, resource_manager: ResourceManager
) -> bool:
    return settings.client.download_new_videos or not resource_manager.is_video(
        resource
    )


def _confirmation_messagebox(resource_count: int, parent: QWidget) -> QMessageBox:
    return QMessageBox(
        QMessageBox.Icon.Question,
        "Many files to download",
        f"You are about to download {resource_count} new files.\n"
        "Do you want to continue?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        parent=parent,
    )
