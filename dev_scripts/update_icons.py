# This file regenerates icons.qrc, rc_icons.py and the icons definition file based on the icons in dark/, light/ and universal/

import subprocess
from pathlib import Path

import xmltodict
import textwrap
from mako.template import Template
from collections import defaultdict


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
    groups = group_icons_by_category(icons)

    template = """
    from .rc_icons import qt_resource_data as _  # Without this, icon data will not be loaded
    from ._icon_type import UniversalIcon, ThemeIcon
    from PySide6.QtGui import QIcon
    
    % for group_name, icons in groups.items():
    # noinspection PyPep8Naming
    class ${group_name}:
        % for icon in sorted(icons):
        ${icon.stem} = QIcon.fromTheme("${icon.parent / icon.stem}")
        % endfor
    
    
    % endfor      
    """

    template = Template(textwrap.dedent(template))
    return template.render(groups=groups)


def group_icons_by_category(icons: list[Path]) -> dict[str, set[Path]]:
    groups: dict[str, set[Path]] = defaultdict(set)

    for icon in icons:
        icon = remove_base_directory(icon)
        icon_category = icon.parts[0]
        groups[icon_category].add(icon)

    return groups


def run_rcc(icons_dir: Path) -> None:
    subprocess.run(
        ["pyside6-rcc", icons_dir / "icons.qrc", "-o", icons_dir / "rc_icons.py"]
    )


def write(file_name: Path, content: str) -> None:
    with open(file_name, "w") as f:
        f.write(content)


def update(icons_dir: Path):
    all_icons: list[Path] = [
        Path(file).relative_to(icons_dir)
        for file in icons_dir.glob(
            "**/*.svg",
        )
    ]
    all_icons.sort()

    write(icons_dir / "icons.qrc", generate_xml(all_icons))
    write(icons_dir / "__init__.py", generate_icon_defs(all_icons))
    run_rcc(icons_dir)
