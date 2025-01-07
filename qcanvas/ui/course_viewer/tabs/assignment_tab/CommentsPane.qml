import QtQuick

Rectangle {
    anchors.fill: parent

    // todo: dark theme and native theme?
    Palette {
        id: pyqtdarktheme
        base: "#f8f9fa"
        accent: "#e02424"
        midlight: "#f8f9fa"
        dark: "#dadce0"
        link: "#e02424"
        text: "#4d5157"
    }

    color: pyqtdarktheme.base

    CommentsList {
        anchors.fill: parent
        model: comments
        palette: pyqtdarktheme
    }
}