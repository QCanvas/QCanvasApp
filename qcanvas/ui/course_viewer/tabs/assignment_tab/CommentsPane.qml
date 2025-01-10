import QtQuick

ThemedRectangle {
    anchors.fill: parent
    color: theme.base

    CommentsList {
        id: commentsList
        anchors.fill: parent
        model: comments
        palette: theme
    }
}
