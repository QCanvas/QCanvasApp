import asyncio
import json
import os
from importlib.metadata import version

import httpx
from packaging.version import Version

from qcanvas.util.constants import package_name


async def do_update():
    await asyncio.to_thread(os.system, f"pip install --upgrade {package_name}")


async def get_newer_version() -> Version | None:
    latest_version = await get_versions()
    installed_version = Version(version(package_name))

    print(f"latest = {latest_version}, installed = {installed_version}")

    if installed_version < latest_version:
        return latest_version
    else:
        return None


async def get_versions() -> Version:
    async with httpx.AsyncClient() as client:
        data = json.loads((await client.get(f"https://pypi.org/pypi/{package_name}/json")).text)
        return Version(data["info"]["version"])
