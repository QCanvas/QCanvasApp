import os
import platform
import sys
from pathlib import Path

is_running_portable = Path(".portable").exists()
is_running_on_windows = platform.system() == "Windows"
is_running_on_linux = platform.system() == "Linux"
_is_nuitka = "__compiled__" in globals()
_is_pyinstaller = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
is_running_as_compiled = _is_nuitka or _is_pyinstaller
is_running_as_flatpak = os.environ.get("container", "") == "flatpak"

__all__ = [
    "is_running_portable",
    "is_running_as_flatpak",
    "is_running_on_linux",
    "is_running_as_compiled",
    "is_running_on_windows",
]
