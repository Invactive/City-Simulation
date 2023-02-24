# ===============================================#
# Topic: Synthetic data generation for object    #
#        detection systems using Unreal Engine 5 #
# Author: Jakub Grzesiak                         #
# University: Poznan University of Technology    #
# Python version: 3.9.7                          #
# ===============================================#

from array import array
from recorder import Recorder
import unreal
import time
import settings
import json
import pathlib
import importlib
importlib.reload(settings)


JOBCOUNTER = 0
QUEUECOUNTER = 0

duration = [1, 3, 10, 20, 30]   # [1, 3, 10, 20, 30]
varDur_20vehs_1cam_100chars_60FPS = {}
ue5recorder = Recorder()

SEQUENCES = ue5recorder.loadSequences(settings.SEQ_DIR)
ue5recorder.deleteLevelSequences(SEQUENCES)

def OnIndividualJobFinishedCallback(params):
    unreal.log("onIndividualJobFinishedCallback")
    print("onIndividualJobFinishedCallback")
    global sTime
    eTime = time.time()
    dTime = eTime - sTime
    global JOBCOUNTER
    print("JOB NUMBER {} FINISHED".format(JOBCOUNTER))
    JOBCOUNTER += 1
    if JOBCOUNTER < len(duration):
        sTime = time.time()

    varDur_20vehs_1cam_100chars_60FPS[duration[JOBCOUNTER-1]] = dTime
    print("varDur_20vehs_1cam_100chars_60FPS", varDur_20vehs_1cam_100chars_60FPS)

def OnQueueFinishedCallback(pipeline_executor, result):
    unreal.log("All sequences rendered. State:" + str(result))
    print("Saving json file in folder" + settings.SAVEDIR_DUR)
    f = open(settings.SAVEDIR_DUR + r"\timeComplexity.json", "w")
    f.write(json.dumps(varDur_20vehs_1cam_100chars_60FPS))
    f.close
    global QUEUECOUNTER
    QUEUECOUNTER += 1
    print("QUEUE NUMBER {} FINISHED".format(QUEUECOUNTER))
    settings.PRESET.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting).use_custom_frame_rate = False

def setSequenceParams(sequences: array, cameras: array, fps: int, time: list):
    idx = 0
    for seq in sequences:
        unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(seq)
        for cam in cameras:
            print("Adding tracks...")
            camera_cut_track = seq.add_master_track(unreal.MovieSceneCameraCutTrack)
            camera_cut_section = camera_cut_track.add_section()
            camera_cut_section.set_start_frame_seconds(0.0)
            camera_cut_section.set_end_frame_seconds(time[idx])

            camera_binding = seq.add_possessable(cam)
            transform_track = camera_binding.add_track(unreal.MovieScene3DAttachTrack)
            transform_section = transform_track.add_section()
            transform_section.set_start_frame_seconds(0.0)
            transform_section.set_end_frame_seconds(time[idx])

            camera_binding_id = seq.make_binding_id(camera_binding, unreal.MovieSceneObjectBindingSpace.LOCAL)
            camera_cut_section.set_camera_binding_id(camera_binding_id)
                    
        frame_rate = unreal.FrameRate(numerator=fps, denominator=1)
        seq.set_display_rate(frame_rate)
        seq.set_playback_start_seconds(0.0)
        seq.set_playback_end_seconds(time[idx])
        seq.set_work_range_start(0.0)
        seq.set_work_range_end(time[idx])
        seq.set_view_range_start(0.0)
        seq.set_view_range_end(time[idx] + 1)
        seq.make_range_seconds(0.0, time[idx])
        unreal.EditorAssetLibrary.save_asset(seq.get_path_name())
        idx += 1

def createRenderQueue(sequences: array, map: unreal.SoftObjectPath, preset: unreal.MoviePipelineMasterConfig):
    MPQsubsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem) 
    pipelineQueue = MPQsubsystem.get_queue()

    jobIter = 0
    for seq in sequences:
        settings.SAVEDIR_DUR += r'\{}s'.format(duration[jobIter]) + r'_20vehs_1cam_100chars_60FPS'
        job = pipelineQueue.allocate_new_job(unreal.MoviePipelineExecutorJob)
        job.map = map
        job.job_name = "Camera" + str(jobIter)
        job.sequence = unreal.SoftObjectPath(seq.get_path_name())
        jobDir = settings.SAVEDIR_DUR + "\\" + str(job.job_name)
        modPreset = ue5recorder.modifyJobPreset(preset, jobDir)
        job.set_configuration(modPreset)
        job.get_configuration().initialize_transient_settings()
        if jobIter == len(duration):
            break
        settings.SAVEDIR_DUR = str(pathlib.Path(settings.SAVEDIR_DUR).parent)
        jobIter += 1

# Clear queue
MPQsubsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem) 
pipelineQueue = MPQsubsystem.get_queue()
if len(pipelineQueue.get_jobs()) != 0:
    pipelineQueue.delete_all_jobs()

cameras = ue5recorder.getCineCameraActors(settings.ACTORS)
ue5recorder.renameCineCameraActors(cameras)
ue5recorder.createLevelSequences(len(duration))
sequences = ue5recorder.loadSequences(settings.SEQ_DIR)
setSequenceParams(sequences, cameras, 60, duration)
createRenderQueue(sequences, settings.WORLD_SOP, settings.PRESET)
ue5recorder.updateWorld()
ue5recorder.setNumOfChars(100)
ue5recorder.setNumOfVehs(20, settings.ACTORS)
ue5recorder.saveLevel()

MPQsubsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem) 
pipelineQueue = MPQsubsystem.get_queue()

global executor
executor = unreal.MoviePipelinePIEExecutor(MPQsubsystem)
executor.on_individual_job_work_finished_delegate.add_callable_unique(OnIndividualJobFinishedCallback)
executor.on_executor_finished_delegate.add_callable_unique(OnQueueFinishedCallback)

global sTime
sTime = time.time()
MPQsubsystem.render_queue_with_executor_instance(executor)
