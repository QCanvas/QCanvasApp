from qtpy.QtGui import QIcon

from ._icon_type import ThemeIcon, UniversalIcon
from .rc_icons import (
    qt_resource_data as _,  # Without this, icon data will not be loaded
)


# noinspection PyPep8Naming
class actions:
    exit = QIcon.fromTheme("actions/exit")
    mark_all_read = QIcon.fromTheme("actions/mark_all_read")
    open_downloads = QIcon.fromTheme("actions/open_downloads")
    quick_login = QIcon.fromTheme("actions/quick_login")
    sync = QIcon.fromTheme("actions/sync")


# noinspection PyPep8Naming
class branding:
    logo_transparent = QIcon.fromTheme("branding/logo_transparent")
    main_icon = QIcon.fromTheme("branding/main_icon")


# noinspection PyPep8Naming
class options:
    auto_download = QIcon.fromTheme("options/auto_download")
    ignore_old = QIcon.fromTheme("options/ignore_old")
    include_videos = QIcon.fromTheme("options/include_videos")
    theme = QIcon.fromTheme("options/theme")


# noinspection PyPep8Naming
class tabs:
    assignments = QIcon.fromTheme("tabs/assignments")
    assignments_new_content = QIcon.fromTheme("tabs/assignments_new_content")
    mail = QIcon.fromTheme("tabs/mail")
    mail_new_content = QIcon.fromTheme("tabs/mail_new_content")
    pages = QIcon.fromTheme("tabs/pages")
    pages_new_content = QIcon.fromTheme("tabs/pages_new_content")


# noinspection PyPep8Naming
class tree_items:
    assignment = QIcon.fromTheme("tree_items/assignment")
    mail = QIcon.fromTheme("tree_items/mail")
    module = QIcon.fromTheme("tree_items/module")
    page = QIcon.fromTheme("tree_items/page")
    semester = QIcon.fromTheme("tree_items/semester")


# noinspection PyPep8Naming
class downloads:
    download_failed = QIcon.fromTheme("downloads/download_failed")
    downloaded = QIcon.fromTheme("downloads/downloaded")
    not_downloaded = QIcon.fromTheme("downloads/not_downloaded")
    unknown = QIcon.fromTheme("downloads/unknown")
