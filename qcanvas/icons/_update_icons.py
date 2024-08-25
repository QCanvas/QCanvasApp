# This file regenerates icons.qrc, rc_icons.py and the icons definition file based on the icons in dark/, light/ and universal/

import glob
import logging
import os
import subprocess
from pathlib import Path
from typing import *

import xmltodict

_logger = logging.getLogger(__name__)


class TempThemeIcon(NamedTuple):
    theme_path: Path


class TempUniversalIcon(NamedTuple):
    theme_path: Path
    full_path: Path


AnyIcon = TempUniversalIcon | TempThemeIcon


def remove_base_directory(path: str | Path) -> Path:
    if isinstance(path, str):
        path = Path(path)

    return Path(*path.parts[1:])


def generate_xml(all_icons: list[str]) -> str:
    xml_dict = {
        "RCC": {
            "@version": "1.0",
            "qresource": {"@prefix": "icons/", "file": all_icons},
        }
    }

    return "<!DOCTYPE RCC>\n" + xmltodict.unparse(
        xml_dict, pretty=True, full_document=False
    )


def generate_icon_defs(icons: list[AnyIcon]) -> str:
    groups = group_icons_by_category(icons)
    classes = [
        generate_group_class(group_name, icons) for group_name, icons in groups.items()
    ]

    return f"""from .rc_icons import qt_resource_data as _  # Without this, icon data will not be loaded
from qtpy.QtGui import QIcon
from ._icon_type import UniversalIcon, ThemeIcon

""" + "\n\n".join(
        classes
    )


def group_icons_by_category(icons: list[AnyIcon]) -> dict[str, set[AnyIcon]]:
    groups: dict[str, set[AnyIcon]] = {}

    for icon in icons:
        theme_path = icon.theme_path.parts
        groups.setdefault(theme_path[0], set())
        groups[theme_path[0]].add(icon)

    return groups


def generate_group_class(group_name: str, icons: set[AnyIcon]) -> str:
    # pascal_case_class_name = "".join([part.title() for part in group_name.split("_")])
    lines = ["# noinspection PyPep8Naming", f"class {group_name}:"]

    for icon in icons:
        path_no_ext = os.path.splitext(icon.theme_path)[0]

        lines.append(f'    {icon.theme_path.stem} = QIcon.fromTheme("{path_no_ext}")')
        # if isinstance(icon, TempThemeIcon):
        #     lines.append(f'    {icon.theme_path.stem} = ThemeIcon("{path_no_ext}")')
        # elif isinstance(icon, TempUniversalIcon):
        #     lines.append(
        #         f'    {icon.theme_path.stem} = UniversalIcon("{path_no_ext}", "{icon.full_path}")'
        #     )
        # else:
        #     raise RuntimeError("Wtf??")

    return "\n".join(lines)


def run_rcc() -> None:
    subprocess.run(["pyside6-rcc", "icons.qrc", "-o", "rc_icons.py"])


def write(file_name: str, content: str) -> None:
    with open(file_name, "w") as f:
        f.write(content)


if __name__ == "__main__":
    theme_icons: list[TempThemeIcon] = []
    universal_icons: list[TempUniversalIcon] = []
    all_icons: list[str] = []

    for file in glob.glob("**/*.svg", recursive=True):
        path = Path(file)

        if path.parts[0] == "universal":
            universal_icons.append(
                TempUniversalIcon(
                    full_path=path, theme_path=remove_base_directory(path)
                )
            )
        else:
            theme_icons.append(TempThemeIcon(theme_path=remove_base_directory(path)))

        all_icons.append(file)

    write("icons.qrc", generate_xml(all_icons))
    write("__init__.py", generate_icon_defs(theme_icons + universal_icons))
    run_rcc()
