import logging

import qcanvas_backend.database.types as db
from qcanvas_backend.net.resources.download.resource_manager import ResourceManager

_logger = logging.getLogger(__name__)


# todo stub for now
class _RM(ResourceManager):
    def on_download_progress(self, resource: db.Resource, current: int, total: int):
        if total == 0 and current == 0:
            _logger.info(f"download of {resource.file_name}: ?%")
        else:
            _logger.info(
                f"download of {resource.file_name}: {(current / total) * 100}%"
            )

    def on_download_failed(self, resource: db.Resource):
        _logger.info(f"download of {resource.file_name} failed")

    def on_download_finished(self, resource: db.Resource):
        _logger.info(f"download of {resource.file_name} finished")
