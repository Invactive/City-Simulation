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

vehs = [1, 5, 10, 30, 50]     # [1, 5, 10, 30, 50]
varVehs_100chars_1cam_60fps_10s = {}
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
    if JOBCOUNTER < len(vehs):
        ue5recorder.setNumOfVehs(vehs[JOBCOUNTER], settings.ACTORS)
        sTime = time.time()
    varVehs_100chars_1cam_60fps_10s[vehs[JOBCOUNTER-1]] = dTime
    print("varVehs_100chars_1cam_60fps_10s", varVehs_100chars_1cam_60fps_10s)

def OnQueueFinishedCallback(pipeline_executor, result):
    unreal.log("All sequences rendered. State:" + str(result))
    print("Saving json file in folder" + settings.SAVEDIR_VEHS)
    f = open(settings.SAVEDIR_VEHS + r"\timeComplexity.json", "w")
    f.write(json.dumps(varVehs_100chars_1cam_60fps_10s))
    f.close
    global QUEUECOUNTER
    QUEUECOUNTER += 1
    print("LAST QUEUE NUMBER {} FINISHED".format(QUEUECOUNTER))

def createRenderQueue(sequences: array, map: unreal.SoftObjectPath, preset: unreal.MoviePipelineMasterConfig, dir: str):
    MPQsubsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem) 
    pipelineQueue = MPQsubsystem.get_queue()
    jobIter = 0
    for seq in sequences:
        job = pipelineQueue.allocate_new_job(unreal.MoviePipelineExecutorJob)
        job.map = map
        job.job_name = "Camera" + str(jobIter)
        job.sequence = unreal.SoftObjectPath(seq.get_path_name())
        jobDir = dir + "\\" + str(job.job_name)
        modPreset = ue5recorder.modifyJobPreset(preset, jobDir)
        job.set_configuration(modPreset)
        jobIter += 1
        job.get_configuration().initialize_transient_settings()
    
# Clear queue
MPQsubsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem) 
pipelineQueue = MPQsubsystem.get_queue()
if len(pipelineQueue.get_jobs()) != 0:
    pipelineQueue.delete_all_jobs()

ue5recorder.setNumOfVehs(vehs[JOBCOUNTER], settings.ACTORS)
ue5recorder.setNumOfChars(100)

for i in vehs:
    ue5recorder.sequenceCreationProcess(fps=60, durationTime=10)
    ue5recorder.updateWorld()
    sequences = ue5recorder.loadSequences(settings.SEQ_DIR)
    ue5recorder.saveLevel()
    settings.SAVEDIR_VEHS += r'\{}vehs'.format(i) + r'_100_chars_1cam_60fps_10s'
    createRenderQueue(sequences, settings.WORLD_SOP, settings.PRESET, settings.SAVEDIR_VEHS)
    settings.SAVEDIR_VEHS = str(pathlib.Path(settings.SAVEDIR_VEHS).parent)
    
global executor
executor = unreal.MoviePipelinePIEExecutor(MPQsubsystem)
executor.on_individual_job_work_finished_delegate.add_callable_unique(OnIndividualJobFinishedCallback)
executor.on_executor_finished_delegate.add_callable_unique(OnQueueFinishedCallback)

global sTime
sTime = time.time()
MPQsubsystem.render_queue_with_executor_instance(executor)
