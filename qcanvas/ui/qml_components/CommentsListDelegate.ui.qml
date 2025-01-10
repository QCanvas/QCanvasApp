

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls

Control {
    padding: 15
    topInset: 5
    bottomInset: 5
    background: Rectangle {
        color: palette.midlight
        radius: 4
        border.color: palette.dark
    }
    clip: true
    height: delegate.height + padding * 2
    anchors {
        left: view.contentItem.left
        right: view.contentItem.right
    }

    contentItem: Item {
        id: delegate
        height: column.height
        anchors {
            left: parent.left
            right: parent.right
            margins: padding
        }

        Column {
            id: column
            anchors {
                left: parent.left
                right: parent.right
            }

            Item {
                height: authorText.height
                anchors {
                    left: parent.left
                    right: parent.right
                }

                Text {
                    id: authorText
                    text: modelData.author
                    clip: true
                    color: palette.text

                    font {
                        pointSize: 12
                        bold: true
                    }
                    anchors {
                        left: parent.left
                    }
                }

                Text {
                    id: commentDate
                    text: modelData.date
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignRight
                    color: palette.text
                    clip: true

                    anchors {
                        left: authorText.right
                        right: parent.right
                        top: parent.top
                        bottom: parent.bottom
                        leftMargin: 5
                    }
                }
            }

            Spacer {
                size: 10
            }

            DecoratedText {
                text: modelData.body
                lineWidth: 2
                anchors {
                    left: parent.left
                    right: parent.right
                }
                content {
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                }
            }

            Spacer {
                size: 10
                visible: modelData.attachments.length > 0
            }

            AttachmentsList {
                id: attachmentsList
                height: contentHeight
                model: modelData.attachments
                interactive: false
                visible: modelData.attachments.length > 0
                anchors {
                    left: parent.left
                    right: parent.right
                }
            }
        }
    }
}
