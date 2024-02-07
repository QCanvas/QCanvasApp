import sys

QT_VERSION = 6

# if sys.modules.get("PySide6.QtCore"):
#     QT_VERSION = 6
# elif sys.modules.get("PySide2.QtCore"):
#     QT_VERSION = 2
# else:
#     QT_VERSION = None
#     raise Exception("Unsupported version of qt")
#
# def set_qt_version():
#     QT_VERSION = 6

def run_app(app):
    if sys.modules.get("PySide6.QtCore"):
        return app.exec()
    else:
        return app.exec_()