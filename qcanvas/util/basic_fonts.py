from qtpy.QtGui import QFont
from qtpy.QtWidgets import QLabel

normal_font = QFont()
bold_font = QFont()
bold_font.setBold(True)


def bold_label(text: str) -> QLabel:
    result = QLabel(text)
    result.setFont(bold_font)
    return result
