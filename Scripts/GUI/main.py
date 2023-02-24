# ===============================================#
# Topic: Synthetic data generation for object    #
#        detection systems using Unreal Engine 5 #
# Author: Jakub Grzesiak                         #
# University: Poznan University of Technology    #
# Python version: 3.9.7                          #
# ===============================================#

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal
import unreal
import sys
from pathlib import Path
import recorder
import settings
import importlib
importlib.reload(settings)


class MainWindow(QObject):
    """
    Main application window.

    Args:
        QObject (QObject): Base class for MainWindow.
    """    
    sliderCharsValueSignal = Signal(int)
    sliderVehsValueSignal = Signal(int)
    sliderFramesValueSignal = Signal(int)
    sliderDurationValueSignal = Signal(int)
    submitBrowseSignal = Signal(str)
    submitPreviewSignal = Signal(str)
    submitStartGenSignal = Signal(bool)
    saveDir = None
    fps = 3
    durationTime = 1
    charsVal = None
    vehsVal = None

    ueRecorder = recorder.Recorder()
    root_window = unreal.LevelEditorSubsystem(name="City_map")
    
    def __init__(self) -> None:
        super().__init__()
    
    @Slot()
    def preview(self) -> None:
        """
        OnClick function called when 'Start Preview' button is pressed.
        Lets user see the world that will be generated.
        """        
        self.ueRecorder.saveLevel()
        if self.ueRecorder.isInPlay():
            self.ueRecorder.stopPreview()
            self.submitPreviewSignal.emit("Start\nPreview")
        else:
            self.ueRecorder.startPreview()
            self.submitPreviewSignal.emit("Stop\nPreview")

    @Slot()
    def goToCredits(self) -> None:
        """
        OnClick function placeholder.
        """      
        pass
    
    @Slot()
    def applyChanges(self) -> None:
        """
        OnClick function called when 'Apply Changes' button is pressed.
        Updates changes in world and creates sequences from cameras.
        """      
        self.ueRecorder.updateWorld()
        self.ueRecorder.sequenceCreationProcess(fps=self.fps, durationTime=self.durationTime)
        self.ueRecorder.saveLevel()

    @Slot()
    def startGen(self) -> None:
        """
        OnClick function called when "Start Generation' button is pressed.
        Creates queue from existing sequences and executes it.
        """      
        if self.saveDir != None:
            self.submitStartGenSignal.emit(True)
            self.ueRecorder.updateWorld()
            sequences = self.ueRecorder.loadSequences(settings.SEQ_DIR)
            self.ueRecorder.saveLevel()
            self.ueRecorder.createRenderQueue(sequences, settings.WORLD_SOP, settings.PRESET, self.saveDir)
            self.ueRecorder.executeRenderQueue()
        else:
            self.submitStartGenSignal.emit(False)

    @Slot()
    def browseFileExplorer(self) -> None:
        """
        OnClick function called when "Browse' button is pressed.
        Lets user pick directory to store output data.
        """        
        self.saveDir = self.ueRecorder.pickDirectory()
        self.submitBrowseSignal.emit(self.saveDir)

    @Slot(int)
    def getSliderCharsVal(self, val: int) -> None:
        """
        Takes user input and sets number of character to generate in world.

        Args:
            val (int): Number of characters to generate.
        """        
        self.sliderCharsValueSignal.emit(val)
        self.ueRecorder.setNumOfChars(val)

    @Slot(int)
    def getSliderVehsVal(self, val: int) -> None:
        """
        Takes user input and sets number of vehicles to generate in world.

        Args:
            val (int): Number of vehicles to generate.
        """        
        self.sliderVehsValueSignal.emit(val)
        self.ueRecorder.setNumOfVehs(val, settings.ACTORS)
        
    @Slot(int)
    def getSliderFramesVal(self, val: int) -> None:
        """
        Takes user input and sets number of frames per second to generate in world.

        Args:
            val (int): Number of characters to generate.
        """        
        self.sliderFramesValueSignal.emit(val)
        self.fps = val        

    @Slot(int)
    def getSliderDurationVal(self, val: int) -> None:
        """
        Takes user input and sets required duration of recording to generate.

        Args:
            val (int): Duration (in seconds) of recording.
        """        
        self.sliderDurationValueSignal.emit(val)
        self.durationTime = val


if __name__ == "__main__":
    if not QGuiApplication.instance():
        app = QGuiApplication(sys.argv)
    else:
        app = QGuiApplication.instance()

    engine = QQmlApplicationEngine()
    main = MainWindow()
    
    engine.rootContext().setContextProperty("backend", main)
    qml_file = Path(__file__).resolve().parent / "qml/main.qml"
    engine.load(qml_file)

    root_window = unreal.LevelEditorSubsystem(name="City_map")
    root_window.set_as_owner(engine.rootObjects()[0].winId())
    
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())

