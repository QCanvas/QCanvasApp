import QtQuick

ThemedRectangle {
    anchors.fill: parent
    color: theme.base

    CommentsList {
        anchors.fill: parent
        model: comments
        palette: theme
    }
}
