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

fps = [10, 30, 60, 90, 120]     # [10, 30, 60, 90, 120]
varFPS_20vehs_1cam_100chars_10s = {}
ue5recorder = Recorder()

def OnIndividualJobFinishedCallback(params):
    unreal.log("onIndividualJobFinishedCallback")
    print("onIndividualJobFinishedCallback")
    global sTime
    eTime = time.time()
    dTime = eTime - sTime
    global JOBCOUNTER
    print("JOB NUMBER {} FINISHED".format(JOBCOUNTER))
    JOBCOUNTER += 1
    if JOBCOUNTER < len(fps):
        sTime = time.time()
    varFPS_20vehs_1cam_100chars_10s[fps[JOBCOUNTER-1]] = dTime
    print("varFPS_20vehs_1cam_100chars_10s", varFPS_20vehs_1cam_100chars_10s)

def OnQueueFinishedCallback(pipeline_executor, result):
    unreal.log("All sequences rendered. State:" + str(result))
    print("Saving json file in folder" + settings.SAVEDIR_FPS)
    f = open(settings.SAVEDIR_FPS + r"\timeComplexity.json", "w")
    f.write(json.dumps(varFPS_20vehs_1cam_100chars_10s))
    f.close
    global QUEUECOUNTER
    QUEUECOUNTER += 1
    print("LAST QUEUE NUMBER {} FINISHED".format(QUEUECOUNTER))
    settings.PRESET.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting).use_custom_frame_rate = False
 
def modifyJobPreset(preset: unreal.MoviePipelineMasterConfig, dir: str, fps: int):
    preset.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting).output_directory = unreal.DirectoryPath(dir)
    preset.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting).use_custom_frame_rate = True
    preset.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting).output_frame_rate = unreal.FrameRate(fps, 1)
    return preset

def modifyFpsPreset(preset: unreal.MoviePipelineMasterConfig, fps: int):
    preset.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting).use_custom_frame_rate = True
    preset.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting).output_frame_rate = unreal.FrameRate(fps, 1)

def createRenderQueue(sequences: array, map: unreal.SoftObjectPath, preset: unreal.MoviePipelineMasterConfig, dir: str, fps: int):
    MPQsubsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem) 
    pipelineQueue = MPQsubsystem.get_queue()
    jobIter = 0
    for seq in sequences:
        job = pipelineQueue.allocate_new_job(unreal.MoviePipelineExecutorJob)
        job.map = map
        job.job_name = "Camera" + str(jobIter)
        job.sequence = unreal.SoftObjectPath(seq.get_path_name())
        jobDir = dir + "\\" + str(job.job_name)
        modPreset = modifyJobPreset(preset, jobDir, fps)
        job.set_configuration(modPreset)
        jobIter += 1
        job.get_configuration().initialize_transient_settings()
    
# Clear queue
MPQsubsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem) 
pipelineQueue = MPQsubsystem.get_queue()
if len(pipelineQueue.get_jobs()) != 0:
    pipelineQueue.delete_all_jobs()

ue5recorder.setNumOfVehs(20, settings.ACTORS)
ue5recorder.setNumOfChars(100)

for i in fps:
    ue5recorder.sequenceCreationProcess(fps=i, durationTime=10)
    ue5recorder.updateWorld()
    sequences = ue5recorder.loadSequences(settings.SEQ_DIR)
    ue5recorder.saveLevel()
    settings.SAVEDIR_FPS += r'\{}FPS'.format(i) + r'_20vehs_1cam_100chars_10s'
    createRenderQueue(sequences, settings.WORLD_SOP, settings.PRESET, settings.SAVEDIR_FPS, i)
    settings.SAVEDIR_FPS = str(pathlib.Path(settings.SAVEDIR_FPS).parent)

global executor
executor = unreal.MoviePipelinePIEExecutor(MPQsubsystem)
executor.on_individual_job_work_finished_delegate.add_callable_unique(OnIndividualJobFinishedCallback)
executor.on_executor_finished_delegate.add_callable_unique(OnQueueFinishedCallback)

global sTime
sTime = time.time()
MPQsubsystem.render_queue_with_executor_instance(executor)

modifyFpsPreset(settings.PRESET, 10)
