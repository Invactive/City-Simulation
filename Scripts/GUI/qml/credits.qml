import QtQuick 2.6
import QtQuick.Window
import QtQuick.Controls 6.3
import QtQuick.Controls.Material 2.12
import QtQml 2.15


Window {
    id: mainWindow
    width: 800
    height: 500
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
        id: authors
        x: 571
        y: 315
        width: 148
        height: 69
        color: "#b8c1ec"
        text: qsTr("Authors:\nJakub Grzesiak\nHubert Furmann")
        anchors.bottom: parent
        anchors.bottomMargin: 150
        anchors.right: parent
        anchors.rightMargin: 150
        font.pixelSize: 20
        wrapMode: Text.WordWrap
        font.styleName: "Regular"
        font.family: "Roboto"
    }

    Text {
        id: supervisor
        x: 571
        y: 397
        width: 184
        height: 69
        color: "#b8c1ec"
        text: qsTr("Supervisor:\ndr inż. Michał Fularz")
        anchors.bottom: parent
        anchors.bottomMargin: 150
        anchors.right: parent
        anchors.rightMargin: 150
        font.pixelSize: 20
        wrapMode: Text.WordWrap
        font.styleName: "Regular"
        font.family: "Roboto"
    }


    Text {
        id: descrText
        x: 55
        y: 40
        width: 700
        height: 344
        color: "#b8c1ec"
        text: qsTr("This appication is a graphical user interface for controlling parameters in synthetic data generator designed for object detection. It is a part of engineering project:\n'Synthetic data generation for object detection systems using Unreal Engine 5'.\n\nThis desktop application allows user to modify:\nNumber of characters from 0 to 1000\nNumber of vehicles from 0 to 50\nNumber of generated frames per second from 3 to 120\nDuration of recording from 1 to 60 seconds\nDirectory to store generated sequences\n\nTo place camera in world create CineCamera actor and move it do desired position. Then, click 'Update World' button to save changes. To generate sequences with choosen parameters click 'Start Generation' button.")
        anchors.bottom: parent
        anchors.bottomMargin: 150
        anchors.right: parent
        anchors.rightMargin: 150
        font.pixelSize: 16
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignTop
        wrapMode: Text.WordWrap
        font.styleName: "Regular"
        font.family: "Roboto"
    }

    Button {
        id: previewBtn
        x: 84
        y: 430
        width: 115
        height: 77
        anchors.left: parent.left
        anchors.leftMargin: 50
        anchors.bottom: parent.bottom
        focus: true
        anchors.bottomMargin: 40
        text: qsTr("Back")
        font.pointSize: 15
        antialiasing: true
        font.bold: true
        font.family: "Roboto"
        highlighted: true
        flat: false

        onClicked: {
            creditsLoader.source = ""
        }
    }

    onClosing: creditsLoader.source = ""


}
