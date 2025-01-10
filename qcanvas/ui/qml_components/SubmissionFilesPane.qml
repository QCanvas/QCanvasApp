import QtQuick

ThemedRectangle {
    anchors.fill: parent
    color: theme.base

    AttachmentsList {
        anchors.fill: parent
        model: submission_files
        palette: theme
    }
}
