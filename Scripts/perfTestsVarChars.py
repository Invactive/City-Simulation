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

chars = [1, 10, 100, 300, 500, 700, 1000]     # [1, 10, 100, 300, 500, 700, 1000]
varChars_20Vehs_1cam_60fps_10s = {}
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
    if JOBCOUNTER < len(chars):
        ue5recorder.setNumOfChars(chars[JOBCOUNTER])
        sTime = time.time()
    varChars_20Vehs_1cam_60fps_10s[chars[JOBCOUNTER-1]] = dTime
    print("varChars_20Vehs_1cam_60fps_10s", varChars_20Vehs_1cam_60fps_10s)

def OnQueueFinishedCallback(pipeline_executor, result):
    unreal.log("All sequences rendered. State:" + str(result))
    print("Saving json file in folder" + settings.SAVEDIR_CHARS)
    f = open(settings.SAVEDIR_CHARS + r"\timeComplexity.json", "w")
    f.write(json.dumps(varChars_20Vehs_1cam_60fps_10s))
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

ue5recorder.setNumOfVehs(20, settings.ACTORS)
ue5recorder.setNumOfChars(chars[JOBCOUNTER])

# Variable chars, 1 cam, 10 fps, 10s duration
for i in chars:
    ue5recorder.sequenceCreationProcess(fps=60, durationTime=10)
    ue5recorder.updateWorld()
    sequences = ue5recorder.loadSequences(settings.SEQ_DIR)
    ue5recorder.saveLevel()
    settings.SAVEDIR_CHARS += r'\{}chars'.format(i) + r'_20vehs_1cam_60fps_10s'
    createRenderQueue(sequences, settings.WORLD_SOP, settings.PRESET, settings.SAVEDIR_CHARS)
    settings.SAVEDIR_CHARS = str(pathlib.Path(settings.SAVEDIR_CHARS).parent)
    
global executor
executor = unreal.MoviePipelinePIEExecutor(MPQsubsystem)
executor.on_individual_job_work_finished_delegate.add_callable_unique(OnIndividualJobFinishedCallback)
executor.on_executor_finished_delegate.add_callable_unique(OnQueueFinishedCallback)

global sTime
sTime = time.time()
MPQsubsystem.render_queue_with_executor_instance(executor)
