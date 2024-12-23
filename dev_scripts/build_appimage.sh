#!/bin/bash

poetry run pyinstaller --hidden-import aiosqlite --onedir -n AppRun qcanvas/__init__.py -y
cp deploy/appimage/* dist/*/
appimagetool dist/*/