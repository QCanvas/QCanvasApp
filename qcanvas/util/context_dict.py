from PySide6.QtQml import QQmlContext


class ContextDict:
    def __init__(self, context: QQmlContext):
        self._context = context

    def __getitem__(self, item):
        return self._context.contextProperty(item)

    def __setitem__(self, key, value):
        self._context.setContextProperty(key, value)
