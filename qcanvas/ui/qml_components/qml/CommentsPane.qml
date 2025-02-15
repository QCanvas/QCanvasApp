import QtQuick

ThemedRectangle {
    anchors.fill: parent

    CommentsList {
        anchors.fill: parent
        model: comments
        palette: theme
    }
}
