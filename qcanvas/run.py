import logging
from logging import INFO, WARNING

import qcanvas.app_start
from qcanvas.util import logs, paths

paths.data_storage().mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filemode="w",
    filename=paths.data_storage() / "debug.log",
    level="WARN",
)

logs.set_levels(
    {
        "qcanvas": INFO,
        "qcanvas.ui": WARNING,
        "qcanvas_backend": INFO,
        "qcanvas.ui.main_ui.status_bar_progress_display": INFO,
    }
)


def main():
    qcanvas.app_start.launch()


if __name__ == "__main__":
    main()
