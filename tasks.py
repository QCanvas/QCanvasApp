from invoke import task
from pathlib import Path


@task
def appimage(c):
    c.run("bash ./dev_scripts/build_appimage.sh")


@task
def update_icons(c):
    import dev_scripts.update_icons as icons

    icons.update(Path("qcanvas/icons/"))
