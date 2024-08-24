# QCanvas

QCanvas is an **unofficial** desktop client for Canvas LMS.

https://codeberg.org/QCanvas/QCanvas

https://github.com/QCanvas/QCanvasApp

# Downloads

<a href='https://flathub.org/apps/io.github.qcanvas.QCanvasApp'>
    <img width='240' alt='Get it on Flathub' src='https://flathub.org/api/badge?svg&locale=en'/>
</a>

You can download a **windows** version from [releases](https://github.com/QCanvas/QCanvasApp/releases)

The appimage version is *not recommended* as it is not a proper portable appimage. It will only work on debian/ubuntu
based distros.

# Development/Run from source

## Prerequisites

- Python 3.12+ (use [pyenv](https://github.com/pyenv/pyenv) if your distro does not have that version)
- [Pipx](https://pipx.pypa.io/stable/) (optional)
- Poetry (recommended to install using `pipx install poetry`)
- [Appimagetool](https://github.com/AppImage/appimagetool) (Only for building the appimage)

## Get started

```bash
git clone https://github.com/QCanvas/QCanvasApp.git
cd QCanvasApp

# Enter shell and run it
poetry shell
poetry install
python qcanvas/run.py

# Alternatively you can run it like this:
poetry install
poetry run python qcanvas/run.py
```

## Build custom AppImage

```bash
bash build_appimage.sh
```