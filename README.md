# QCanvas

QCanvas is an **unofficial** desktop client for Canvas LMS.

https://codeberg.org/QCanvas/QCanvas

https://github.com/QCanvas/QCanvasApp

# Downloads

<a href='https://flathub.org/apps/io.github.qcanvas.QCanvasApp'>
    <img width='240' alt='Get it on Flathub' src='https://flathub.org/api/badge?svg&locale=en'/>
</a>

You can download a **windows** version from [releases](https://github.com/QCanvas/QCanvasApp/releases)

An appimage version is also available from releases but is not recommended.

# Development/Run from source

## Prerequisites

- Python 3.12
- Poetry

## Get started

```bash
git clone https://github.com/QCanvas/QCanvasApp.git
cd QCanvasApp

# Install packages and stuff
poetry install --with flatpak-exclude

# Run QCanvas (If you run `poetry shell`, you can drop the `poetry run` part)
poetry run qcanvas
# Alternative
poetry run python -m qcanvas
```

## Build custom AppImage

> [!WARNING]
> This is not recommended as the appimage produced by this process isn't a proper appimage. It's just a pyinstaller build bundled as an appimage.

> [!IMPORTANT]
> You will need [Appimagetool](https://github.com/AppImage/appimagetool)

```bash
bash ./dev_scripts/build_appimage
```