import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    property alias text: content.text
    property int lineWidth: 3
    property color lineColour: palette.accent
    property alias content: content

    Layout.fillWidth: true
    height: content.contentHeight
    clip: true

    Item {
        anchors.fill: parent
        height: content.contentHeight

        Rectangle {
            id: decoration
            width: lineWidth
            color: lineColour
            radius: 1
            anchors {
                left: parent.left
                top: parent.top
                bottom: parent.bottom
            }
        }

        Text/*Edit*/ {
            id: content
            Layout.fillWidth: true
            color: palette.text
            //readOnly: true
            //textFormat: TextEdit.AutoText
            anchors {
                left: decoration.right
                leftMargin: 10
                right: parent.right
            }
        }
    }
}
