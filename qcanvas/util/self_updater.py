import asyncio
import json
import os
from importlib.metadata import version

import httpx
from packaging.version import Version

from qcanvas.util.constants import package_name

# When true, signals that the program should be restarted when it closes next
restart_flag = False


async def do_update() -> None:
    """
    Updates the qcanvas package and sets the restart flag.
    The restart flag is passed back to the launcher script as a return code.
    """
    global restart_flag
    await asyncio.to_thread(os.system, f"pip install --upgrade {package_name}")
    restart_flag = True


async def get_newer_version() -> tuple[Version | None, Version | None] | None:
    """
    Check for a newer version of qcanvas
    Returns
    -------
    tuple
        A tuple, where the first item is the latest version and the second item is the installed version. If the installed
        version is up-to-date, then the first item is None
    """
    latest_version = await get_latest_version()
    installed_version = Version(version(package_name))

    print(f"latest = {latest_version}, installed = {installed_version}")

    if installed_version < latest_version:
        return latest_version, installed_version
    else:
        return None, installed_version


async def get_latest_version() -> Version:
    """
    Retrieves the latest version of the package from pypi
    Returns
    -------
    Version
        The latest version of qcanvas on pypi
    """
    async with httpx.AsyncClient() as client:
        data = json.loads((await client.get(f"https://pypi.org/pypi/{package_name}/json")).text)
        return Version(data["info"]["version"])
