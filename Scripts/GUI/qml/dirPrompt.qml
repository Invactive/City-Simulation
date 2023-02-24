import QtQuick 2.6
import QtQuick.Window
import QtQuick.Controls 6.3
import QtQuick.Controls.Material 2.12
import QtQml 2.15


Window {
    id: mainWindow
    width: 400
    height: 200
    maximumHeight: height
    maximumWidth: width
    minimumHeight: height
    minimumWidth: width
    visible: true
    title: qsTr("Synthtetic Data Generator")
    color: "#232946"
    flags: Qt.Window

    MouseArea {
        anchors.fill: parent
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        onClicked: forceActiveFocus()
    }

    Text {
        id: descrText
        color: "#b8c1ec"
        text: qsTr("Choose directory to save images before starting generation!")
        anchors.fill: parent
        anchors.rightMargin: 20
        anchors.bottomMargin: 20
        anchors.leftMargin: 20
        anchors.topMargin: 20
        font.pixelSize: 20
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignTop
        wrapMode: Text.WordWrap
        font.styleName: "Regular"
        font.family: "Roboto"
    }

    onClosing: promptLoader.source = ""

    Button {
        id: backBtn
        y: 0
        width: 100
        height: 50
        text: qsTr("OK")
        anchors.left: parent.horizontalCenter
        anchors.bottom: parent.bottom
        antialiasing: true
        font.pixelSize: 20
        anchors.leftMargin: -50
        anchors.bottomMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter
        transformOrigin: Item.Bottom
        focus: true
        font.bold: true
        font.weight: Font.DemiBold
        font.family: "Roboto"
        highlighted: true
        flat: false

        onClicked: {
            promptLoader.source = ""
        }
    }
}
