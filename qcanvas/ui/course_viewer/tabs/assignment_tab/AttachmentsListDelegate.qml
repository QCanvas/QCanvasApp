import QtQuick
import QtQuick.Layouts

Item {
    id: delegate
    height: childrenRect.height
    anchors {
        left: parent.left
        right: parent.right
    }

    ColumnLayout {
        spacing: 0

        anchors {
            left: parent.left
            right: parent.right
        }

        RowLayout {
            height: childrenRect.implicitHeight
            Layout.fillWidth: true
            spacing: 10

            Image {
                function attachmentIcon(downloadStatus) {
                    switch(downloadStatus)
                    {
                        case "DOWNLOADED":
                            return "qrc:///icons/universal/downloads/downloaded.svg";
                        case "FAILED":
                            return "qrc:///icons/universal/downloads/download_failed.svg";
                        case "NOT_DOWNLOADED":
                            return "qrc:///icons/universal/downloads/not_downloaded.svg";
                        default:
                            return "qrc:///icons/universal/downloads/unknown.svg"
                    }
                }

                id: fileIcon
                source: attachmentIcon(modelData.download_state)
                fillMode: Image.PreserveAspectFit
                sourceSize.height: 17
                sourceSize.width: 17
            }

            Text {
                id: file_name_text
                text: modelData.file_name
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                Layout.fillWidth: true
                font.underline: true
                color: palette.link

                MouseArea {
                    id: textClickArea
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    hoverEnabled: true
                }
            }
        }

        Spacer {
            size: 5
            visible: index !== count - 1
        }
    }

    Connections {
        target: textClickArea

        function onClicked() {
            modelData.opened(modelData.resource_id)
        }
    }
}
