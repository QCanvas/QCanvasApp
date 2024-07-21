import logging
from logging import INFO, WARNING

import qcanvas.app_start
from qcanvas.util import paths, logs

paths.data_storage().mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=paths.data_storage() / "debug.log",
    level="WARN",
)

logs.set_levels({"qcanvas": INFO, "qcanvas.ui": WARNING, "qcanvas_backend": INFO})

qcanvas.app_start.launch()
