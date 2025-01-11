#!/bin/bash

poetry run pyinstaller --hidden-import aiosqlite --onedir -n AppRun qcanvas/__init__.py --collect-all libqcanvas.alembic
cp deploy/appimage/* dist/*/
appimagetool dist/*/