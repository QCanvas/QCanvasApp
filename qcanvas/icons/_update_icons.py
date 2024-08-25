# This file regenerates icons.qrc, rc_icons.py and the icons definition file based on the icons in dark/, light/ and universal/

import glob
import logging
import os
import subprocess
from pathlib import Path

import xmltodict

_logger = logging.getLogger(__name__)


def remove_base_directory(path: str | Path) -> Path:
    if isinstance(path, str):
        path = Path(path)

    return Path(*path.parts[1:])


def generate_xml(all_icons: list[Path]) -> str:
    xml_dict = {
        "RCC": {
            "@version": "1.0",
            "qresource": {"@prefix": "icons/", "file": all_icons},
        }
    }

    return "<!DOCTYPE RCC>\n" + xmltodict.unparse(
        xml_dict, pretty=True, full_document=False
    )


def generate_icon_defs(icons: list[Path]) -> str:
    icons_base_removed = [remove_base_directory(icon) for icon in icons]
    groups = group_icons_by_category(icons_base_removed)
    classes = [
        generate_group_class(group_name, icons) for group_name, icons in groups.items()
    ]

    return f"""from .rc_icons import qt_resource_data as _  # Without this, icon data will not be loaded
from qtpy.QtGui import QIcon
from ._icon_type import UniversalIcon, ThemeIcon

""" + "\n\n".join(
        classes
    )


def group_icons_by_category(icons: list[Path]) -> dict[str, set[Path]]:
    groups: dict[str, set[Path]] = {}

    for icon in icons:
        icon_category = icon.parts[0]
        groups.setdefault(icon_category, set())
        groups[icon_category].add(icon)

    return groups


def generate_group_class(group_name: str, icons: set[Path]) -> str:
    # pascal_case_class_name = "".join([part.title() for part in group_name.split("_")])
    lines = ["# noinspection PyPep8Naming", f"class {group_name}:"]

    for icon in sorted(icons):
        path_no_ext = os.path.splitext(icon)[0]
        lines.append(f'    {icon.stem} = QIcon.fromTheme("{path_no_ext}")')

    return "\n".join(lines)


def run_rcc() -> None:
    subprocess.run(["pyside6-rcc", "icons.qrc", "-o", "rc_icons.py"])


def write(file_name: str, content: str) -> None:
    with open(file_name, "w") as f:
        f.write(content)


if __name__ == "__main__":
    all_icons: list[Path] = [
        Path(file) for file in glob.glob("**/*.svg", recursive=True)
    ]
    all_icons.sort()

    write("icons.qrc", generate_xml(all_icons))
    write("__init__.py", generate_icon_defs(all_icons))
    run_rcc()
