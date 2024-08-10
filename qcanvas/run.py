# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --windows-icon-from-ico=./deploy/windows/qcanvas.ico
# nuitka-project: --windows-console-mode=attach
# nuitka-project: --linux-icon=deploy/appimage/qcanvas.svg
# nuitka-project: --standalone
# nuitka-project: --include-module=yt_dlp

# Anti-bloat

##########################################################
# nuitka-project: --include-package=aiosqlite
# nuitka-project: --nofollow-import-to=aiosqlite.tests.*
##########################################################
# nuitka-project: --nofollow-import-to=rich
##########################################################
# nuitka-project: --nofollow-import-to=sqlalchemy.dialects.mssql
# nuitka-project: --nofollow-import-to=sqlalchemy.dialects.postgresql
# nuitka-project: --nofollow-import-to=sqlalchemy.dialects.oracle
# nuitka-project: --nofollow-import-to=sqlalchemy.dialects.mysql
##########################################################
# nuitka-project: --nofollow-import-to=rich
##########################################################
# nuitka-project: --nofollow-import-to=yt_dlp.extractor.lazy_extractors

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
