#!/bin/bash

poetry run pyinstaller --hidden-import aiosqlite --onedir -n AppRun qcanvas/run.py -y
cp deploy/appimage/* dist/*/
appimagetool dist/*/