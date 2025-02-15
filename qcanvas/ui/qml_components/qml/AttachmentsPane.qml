import QtQuick

ThemedRectangle {
    anchors.fill: parent

    AttachmentsList {
        anchors.fill: parent
        model: submission_files
        palette: theme
    }
}
