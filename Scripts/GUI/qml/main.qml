import QtQuick 2.6
import QtQuick.Window
import QtQuick.Controls 6.3
import QtQuick.Controls.Material 2.12
import QtQml 2.15


Window {
    Connections{
        target: backend

        function onSliderCharsValueSignal(val){
            valCrowdCharsInput.text = val
        }

        function onSliderVehsValueSignal(val){
            valVehsInput.text = val
        }

        function onSliderFramesValueSignal(val){
            valFramesInput.text = val
        }

        function onSliderDurationValueSignal(val){
            valDurationInput.text = val
        }

        function onSubmitBrowseSignal(pth){
            currentSavePathText.text = pth
        }

        function onSubmitPreviewSignal(txt){
            previewBtn.text = txt
        }

        function onSubmitStartGenSignal(vis){
            if(vis === false){
                promptLoader.source = "dirPrompt.qml"
            }
        }
    }

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
        id: headerText
        anchors.top: parent.top
        anchors.margins: 10
        color: "#b8c1ec"
        text: qsTr("Synthetic Data Generator")
        anchors.left: parent.left
        anchors.right: parent.right
        font.pixelSize: 28
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
        font.styleName: "Regular"
        font.weight: Font.Bold
        font.family: "Roboto"
    }

    Text {
        id: descText
        height: 50
        color: "#b8c1ec"
        text: qsTr("Engineering Thesis Project: Synthetic data generation for object detection systems\nusing Unreal Engine 5")
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: headerText.bottom
        font.pixelSize: 20
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
        anchors.topMargin: 10
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        font.weight: Font.DemiBold
        font.family: "Roboto"
    }

    Text {
        id: numCrowdCharsText
        x: 100
        y: 140
        color: "#b8c1ec"
        text: qsTr("Number of characters to spawn")
        anchors.top: descText.bottom
        anchors.topMargin: 15
        font.pixelSize: 20
        wrapMode: Text.WordWrap
        font.styleName: "Regular"
        font.family: "Roboto"
    }

    Slider {
        id: numCrowdCharsSlider
        x: 560
        anchors.right: parent.right
        focus: true
        live: true
        pressed: false
        antialiasing: true
        focusPolicy: Qt.NoFocus
        anchors.top: descText.bottom
        anchors.topMargin: 15
        snapMode: RangeSlider.SnapAlways
        stepSize: 1
        to: 1000
        anchors.rightMargin: 60
        y: 140
        width: 250
        height: 24
        value: 0

        onValueChanged: {
            backend.getSliderCharsVal(numCrowdCharsSlider.value)
        }
    }

    Text {
        id: numVehsText
        x: 100
        anchors.top: numCrowdCharsText.bottom
        anchors.topMargin: 20
        color: "#b8c1ec"
        text: qsTr("Number of vehicles to spawn")
        font.pixelSize: 20
        wrapMode: Text.WordWrap
        font.styleName: "Regular"
        font.family: "Roboto"
    }

    Slider {
        id: numVehsSlider
        anchors.right: parent.right
        focus: true
        pressed: false
        antialiasing: true
        focusPolicy: Qt.NoFocus
        anchors.top: numCrowdCharsSlider.bottom
        anchors.topMargin: 20
        snapMode: RangeSlider.SnapAlways
        stepSize: 1
        to: 50
        anchors.rightMargin: 60
        y: 184
        width: 250
        height: 24
        value: 0

        onValueChanged: {
            backend.getSliderVehsVal(numVehsSlider.value)
        }
    }

    Text {
        id: numFramesText
        x: 100
        anchors.top: numVehsText.bottom
        anchors.topMargin: 20
        color: "#b8c1ec"
        text: qsTr("Number of frames per second")
        font.pixelSize: 20
        wrapMode: Text.WordWrap
        font.styleName: "Regular"
        font.family: "Roboto"
    }

    Slider {
        id: numFramesSlider
        anchors.right: parent.right
        focus: true
        pressed: false
        antialiasing: true
        focusPolicy: Qt.NoFocus
        anchors.top: numVehsSlider.bottom
        anchors.topMargin: 20
        snapMode: RangeSlider.SnapAlways
        stepSize: 1
        from: 3
        to: 120
        anchors.rightMargin: 60
        y: 228
        width: 250
        height: 24
        value: 0

        onValueChanged: {
            backend.getSliderFramesVal(numFramesSlider.value)
        }
    }

    Text {
        id: numDurationText
        x: 100
        anchors.top: numFramesText.bottom
        anchors.topMargin: 20
        color: "#b8c1ec"
        text: qsTr("Duration time of recorded sequence [s]")
        font.pixelSize: 20
        wrapMode: Text.WordWrap
        font.styleName: "Regular"
        font.family: "Roboto"
    }

    Slider {
        id: numDurationSlider
        anchors.right: parent.right
        focus: true
        pressed: false
        antialiasing: true
        focusPolicy: Qt.NoFocus
        snapMode: RangeSlider.SnapAlways
        anchors.top: numFramesSlider.bottom
        anchors.topMargin: 20
        stepSize: 1
        from: 1
        to: 300
        anchors.rightMargin: 60
        y: 228
        width: 250
        height: 24
        value: 0

        onValueChanged: {
            backend.getSliderDurationVal(numDurationSlider.value)
        }
    }

    TextInput {
        id: valDurationInput
        x: 825
        y: 274
        width: 35
        height: 20
        font.pixelSize: 20
        antialiasing: true
        anchors.top: valFramesInput.bottom
        anchors.topMargin: 25
        anchors.left: numCrowdCharsSlider.right
        font.family: "Roboto"
        color: "#b8c1ec"
        text: qsTr("1")
        selectByMouse: true
        activeFocusOnPress: true
        wrapMode: Text.WordWrap
        validator: IntValidator {bottom: 1; top: 300}

        onEditingFinished: {
            numDurationSlider.value = valDurationInput.text
        }
    }

    Button {
        id: browseBtn
        x: 565
        width: 100
        height: 33
        anchors.top: numDurationSlider.bottom
        anchors.topMargin: 11
        text: qsTr("Browse")
        antialiasing: true
        font.pixelSize: 12
        focus: true
        font.weight: Font.DemiBold
        font.family: "Roboto"
        highlighted: true
        flat: false

        onClicked: {
            backend.browseFileExplorer()
        }
    }

    Text {
        id: currentSavePathText
        anchors.top: browseBtn.bottom
        anchors.topMargin: 10
        anchors.left: numFramesSlider.left
        anchors.leftMargin: -40
        anchors.right: numFramesSlider.right
        anchors.rightMargin: -40
        color: "#b8c1ec"
        text: qsTr("")
        font.pixelSize: 15
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignHCenter
        font.styleName: "Regular"
        font.family: "Roboto"
    }

    Text {
        id: savePathText
        x: 100
        anchors.top: numDurationText.bottom
        anchors.topMargin: 20
        color: "#b8c1ec"
        text: qsTr("Path to save images")
        font.pixelSize: 20
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
        text: qsTr("Start\nPreview")
        font.pointSize: 15
        antialiasing: true
        font.bold: true
        font.family: "Roboto"
        highlighted: true
        flat: false

        onClicked: {
            backend.preview()
        }
    }

    Button {
        signal goToCredits()
        id: creditsBtn
        x: 217
        width: 115
        height: 77
        anchors.left: previewBtn.right
        anchors.leftMargin: 80
        anchors.bottom: parent.bottom
        focus: true
        anchors.bottomMargin: 40
        text: qsTr("Credits")
        font.pointSize: 15
        antialiasing: true
        font.bold: true
        font.family: "Roboto"
        highlighted: true
        flat: false
        Loader {
            id: creditsLoader
        }

        onClicked: {
            backend.goToCredits()
            creditsLoader.source = "credits.qml"
        }
    }

    Button {
        signal applyChanges()
        id: applyBtn
        x: 560
        y: 413
        width: 115
        height: 77
        anchors.right: startBtn.left
        anchors.rightMargin: 80
        anchors.bottom: parent.bottom
        focus: true
        anchors.bottomMargin: 40
        text: qsTr("Update\nCameras")
        font.pointSize: 15
        antialiasing: true
        font.bold: true
        font.family: "Roboto"
        highlighted: true
        flat: false

        onClicked: {
            backend.applyChanges()
        }
    }

    Button {
        signal startGen()
        id: startBtn
        x: 452
        y: 364
        width: 115
        height: 77
        anchors.right: parent.right
        anchors.rightMargin: 50
        anchors.bottom: parent.bottom
        focus: true
        anchors.bottomMargin: 40
        text: qsTr("Start\nGeneration")
        font.pointSize: 15
        antialiasing: true
        font.bold: true
        font.family: "Roboto"
        highlighted: true
        flat: false
        Loader {
            id: promptLoader
        }

        onClicked: {
            backend.startGen()
        }
    }

    TextInput {
        id: valCrowdCharsInput
        x: 816
        y: 142
        width: 35
        height: 20
        anchors.top: descText.bottom
        anchors.topMargin: 16
        anchors.left: numCrowdCharsSlider.right
        font.pixelSize: 20
        selectByMouse: true
        cursorVisible: false
        font.family: "Roboto"
        color: "#b8c1ec"
        text: qsTr("0")
        activeFocusOnPress: true
        wrapMode: Text.WordWrap
        validator: IntValidator {bottom: 0; top: 300}

        onEditingFinished: {
            numCrowdCharsSlider.value = valCrowdCharsInput.text
        }
    }

    TextInput {
        id: valVehsInput
        x: 816
        y: 186
        width: 35
        height: 20
        text: qsTr("0")
        anchors.top: valCrowdCharsInput.bottom
        anchors.topMargin: 25
        anchors.left: numCrowdCharsSlider.right
        selectByMouse: true
        font.pixelSize: 20
        antialiasing: true
        font.family: "Roboto"
        color: "#b8c1ec"
        wrapMode: Text.WordWrap
        validator: IntValidator {bottom: 0; top: 300}

        onEditingFinished: {
            numVehsSlider.value = valVehsInput.text
        }
    }

    TextInput {
        id: valFramesInput
        x: 816
        y: 230
        width: 35
        height: 20
        font.pixelSize: 20
        antialiasing: true
        anchors.top: valVehsInput.bottom
        anchors.topMargin: 25
        anchors.left: numCrowdCharsSlider.right
        font.family: "Roboto"
        color: "#b8c1ec"
        text: qsTr("3")
        selectByMouse: true
        activeFocusOnPress: true
        wrapMode: Text.WordWrap
        validator: IntValidator {bottom: 3; top: 240}

        onEditingFinished: {
            numFramesSlider.value = valFramesInput.text
        }
    }
}
