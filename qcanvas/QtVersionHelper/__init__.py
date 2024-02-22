import sys
from typing import Any

try:
    import PySide6.QtCore

    QT_VERSION = 6
except ImportError:
    try:
        import PySide2.QtCore

        QT_VERSION = 5
    except ImportError:
        raise Exception("Unsupported version of qt")


def run_app(app: Any) -> Any:
    """
    Runs a QApplication

    Parameters
    ----------
    app : QApplication
        The app to run
    """
    if sys.modules.get("PySide6.QtCore"):
        return app.exec()
    else:
        return app.exec_()
