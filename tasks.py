from invoke import task, Context
from pathlib import Path


@task
def appimage(c):
    c.run("bash ./dev_scripts/build_appimage.sh")


@task
def update_icons(c):
    import dev_scripts.update_icons as icons

    icons.update(Path("qcanvas/icons/"))


@task
def push_all(c: Context):
    out = c.run("git remote", hide=True).stdout
    for remote in out.splitlines():
        c.run(f"git push {remote}")
