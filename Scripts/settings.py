# ===============================================#
# Topic: Synthetic data generation for object    #
#        detection systems using Unreal Engine 5 #
# Author: Jakub Grzesiak                         #
# University: Poznan University of Technology    #
# Python version: 3.9.7                          #
# ===============================================#

# Global variables from Unreal Engine 5
import unreal


# Input USERNAME and SAVEDIR to create output directory for images
USERNAME = "X"
SAVEDIR = r'D:\TestyV2\{}'.format(USERNAME)

SAVEDIR_CHARS = SAVEDIR + r"\varCharacters"
SAVEDIR_VEHS = SAVEDIR + r"\varVehicles"
SAVEDIR_FPS = SAVEDIR + r"\varFPS"
SAVEDIR_DUR = SAVEDIR + r"\varDuration"
SAVEDIR_CAMS = SAVEDIR + r"\varCams"

SEQ_DIR = '/Game/Cinematics/LevelSequences'
ACTORS = unreal.EditorActorSubsystem().get_all_level_actors()
WORLD = unreal.UnrealEditorSubsystem().get_editor_world()
WORLD_SOP = unreal.SoftObjectPath(WORLD.get_path_name())
PRESET = unreal.load_asset(
        '/Game/Cinematics/Utils/RecordingPresetBase.RecordingPresetBase'
)
