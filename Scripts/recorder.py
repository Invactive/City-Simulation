# ===============================================#
# Topic: Synthetic data generation for object    #
#        detection systems using Unreal Engine 5 #
# Author: Jakub Grzesiak                         #
# University: Poznan University of Technology    #
# Python version: 3.9.7                          #
# ===============================================#

from array import array
import tkinter
from tkinter import filedialog
import unreal
import time
import settings
import importlib
importlib.reload(settings)
import random


class Recorder:
    """
    Class containing all the functions required to generate synthetic data from Unreal Engine 5.
    Uses Unreal Python API to connect and interact with editor.
    """    

    def __init__(self) -> None:
            unreal.log("Recorder initialized.")

    def getCineCameraActors(self, actors: array) -> array:
        """
        Gets all CineCamera actors from currently running world.

        Args:
            actors (array): Array of all actors in world.

        Returns:
            array: Array of CineCamera actors.
        """        
        CineCameraActors = []
        for actor in actors:
            if actor.__class__ == unreal.CineCameraActor:
                CineCameraActors.append(actor)
        return CineCameraActors

    def renameCineCameraActors(self, cameras: array) -> None:
        """
        Renames all CineCamera actors to match them with sequences.

        Args:
            cameras (array): Array of CineCamera actors.
        """        
        i = 0
        for cam in cameras:
            name = unreal.StringLibrary.concat_str_str("Camera", unreal.StringLibrary.conv_int_to_string(i))
            cam.rename(name)
            i += 1

    def loadSequences(self, seqDir: str) -> array:
        """
        Loads all existing sequences and appends the to an array. 

        Args:
            seqDir (str): Path to Unreal Engine directory that contains sequences.
                          Example path: '/Game/Cinematics/LevelSequences'.

        Returns:
            array: Array of sequences existing in given directory.
        """        
        levelSequences = []
        sequencesPaths = unreal.EditorAssetLibrary().list_assets(seqDir)
        for seq in sequencesPaths:
            levelSequences.append(unreal.load_asset(seq))
        return levelSequences

    def updateWorld(self) -> None:
        """
        Updates all existing actors in current world.
        Renames CineCamera actors.
        """        
        actors = unreal.EditorActorSubsystem().get_all_level_actors()
        world = unreal.UnrealEditorSubsystem().get_editor_world()
        worldSop = unreal.SoftObjectPath(world.get_path_name())
        preset = unreal.load_asset(
            '/Game/Cinematics/Utils/RecordingPresetBase.RecordingPresetBase'
        )
        self.renameCineCameraActors(self.getCineCameraActors(actors))

    def deleteLevelSequences(self, sequences: array) -> None:
        """
        Deletes all previously created sequence assets.

        Args:
            sequences (array): Array of existing sequences.
        """        
        for seq in sequences:
            unreal.EditorAssetLibrary().delete_asset(seq.get_path_name())

    def createLevelSequences(self, qty: int) -> array:
        """
        Creates new LevelSequences with proper names.
        Example name: 'Camera0Sequence'

        Args:
            qty (int): Number of sequences to create.

        Returns:
            array: Array of new sequences.
        """        
        sequences = []
        prefix = "Camera"
        suffix = "Sequence"
        for i in range(qty):
            asset_name = unreal.StringLibrary.concat_str_str(prefix, unreal.StringLibrary.conv_int_to_string(i))
            asset_name = unreal.StringLibrary.concat_str_str(asset_name, suffix)
            seq = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name, settings.SEQ_DIR, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
            sequences.append(seq)
        return sequences

    def renameLevelSequences(self, sequences: array) -> None:
        """
        Renames LevelSequences in case of user change in editor.
        Example name: 'Camera0Sequence'

        Args:
            sequences (array): Array of renamed sequences.
        """        
        i = 0
        prefix = "Camera"
        suffix = "Sequence"
        for seq in sequences:
            name = unreal.StringLibrary.concat_str_str(prefix, unreal.StringLibrary.conv_int_to_string(i))
            name = unreal.StringLibrary.concat_str_str(name, suffix)
            seq.rename(name)
            i += 1

    def setSequenceParams(self, sequences: array, cameras: array, fps: int, time: float) -> None:
        """
        Sets all required sequence parameters.
        Binds proper tracks from cameras to sequences.
        Prepares sequences to process of data generation.
        Saves given sequences.

        Args:
            sequences (array): Array of existing sequences.
            cameras (array): Array of existing cameras.
            fps (int): Number of frames per second to generate.
            time (float): Duration of sequence to generate.
        """        
        for seq in sequences:
            unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(seq)
            for cam in cameras:
                if int("".join(filter(str.isdigit, cam.get_name()))) is int("".join(filter(str.isdigit, seq.get_name()))) and not seq.get_master_tracks():
                    print("Adding tracks...")
                    camera_cut_track = seq.add_master_track(unreal.MovieSceneCameraCutTrack)
                    camera_cut_section = camera_cut_track.add_section()
                    camera_cut_section.set_start_frame_seconds(0.0)
                    camera_cut_section.set_end_frame_seconds(time)

                    camera_binding = seq.add_possessable(cam)
                    transform_track = camera_binding.add_track(unreal.MovieScene3DAttachTrack)
                    transform_section = transform_track.add_section()
                    transform_section.set_start_frame_seconds(0.0)
                    transform_section.set_end_frame_seconds(time)

                    camera_binding_id = seq.make_binding_id(camera_binding, unreal.MovieSceneObjectBindingSpace.LOCAL)
                    camera_cut_section.set_camera_binding_id(camera_binding_id)
                        
            frame_rate = unreal.FrameRate(numerator=fps, denominator=1)
            seq.set_display_rate(frame_rate)
            seq.set_playback_start_seconds(0.0)
            seq.set_playback_end_seconds(time)
            seq.set_work_range_start(0.0)
            seq.set_work_range_end(time)
            seq.set_view_range_start(0.0)
            seq.set_view_range_end(time + 1)
            seq.make_range_seconds(0.0, time)
            unreal.EditorAssetLibrary.save_asset(seq.get_path_name())

    def sequenceCreationProcess(self, fps: int, durationTime: float) -> array:
        """
        Prepares cameras and sequences to generate data.
        After preparation, sequences are ready to put into movie render queue.  

        Args:
            fps (int): Number of frames per second to generate.
            durationTime (int): Duration of sequence to generate.

        Returns:
            array: Array of prepared sequences.
        """        
        cameras = self.getCineCameraActors(settings.ACTORS)
        self.renameCineCameraActors(cameras)
        sequences = self.loadSequences(settings.SEQ_DIR)
        self.deleteLevelSequences(sequences)
        self.createLevelSequences(len(cameras))
        sequences = self.loadSequences(settings.SEQ_DIR)
        self.setSequenceParams(sequences, cameras, fps, durationTime)
        return sequences

    def setNumOfChars(self, qty: int) -> None:
        """
        Sets number of characters (humans) to exist during generation process.

        Args:
            qty (int): Number of characters.
        """        
        for actor in settings.ACTORS:
            if actor.__class__ == unreal.MassSpawner:
                actor.set_editor_property('count', qty)

    def setNumOfVehs(self, qty: int, actors: array) -> None:
        """
        Sets number of vehicles (cars) to exist during generation process.
        Shuffles list of available cars to randomize which cars should be hidden during generation process.
        
        Args:
            qty (int): Number of vehicles.
            actors (array): Array of all actors in world.
        """        
        cars = []
        for actor in actors:
            if "WheeledVehiclePawn" in str(actor.__class__):
                actor.set_actor_hidden_in_game(True)
                cars.append(actor)
        random.shuffle(cars)
        for i in range(qty):
            cars[i].set_actor_hidden_in_game(False)

    def startPreview(self) -> None:
        """
        Starts in-editor preview of the world.
        """        
        unreal.LevelEditorSubsystem().editor_play_simulate()

    def stopPreview(self) -> None:
        """
        Stops in-editor preview of the world.
        """        
        unreal.LevelEditorSubsystem().editor_request_end_play()

    def saveLevel(self) -> None:
        """
        Saves all changes made in the world.
        """        
        unreal.LevelEditorSubsystem().save_all_dirty_levels()

    def isInPlay(self) -> bool:
        """
        Cheks if editor is in play (simulation) mode.

        Returns:
            bool: State of editor.
        """              
        return unreal.LevelEditorSubsystem().is_in_play_in_editor()

    def modifyJobPreset(self, preset: unreal.MoviePipelineMasterConfig, dir: str) -> unreal.MoviePipelineMasterConfig:
        """
        Modifies output directory in BasicPreset.

        Args:
            preset (unreal.MoviePipelineMasterConfig): Preset to modify.
            dir (str): Output directory to store generated sequences.

        Returns:
            unreal.MoviePipelineMasterConfig: MoviePipelineMasterConfig preset object that contains parameters.
        """        
        preset.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting).output_directory = unreal.DirectoryPath(dir)
        return preset

    def OnIndividualJobFinishedCallback(self, params: any) -> None:
        """
        Callback delegate called after job sequence from queue finish.
        Prints time spent on generating sequence of particular job into Unreal Engine Output Log.

        Args:
            params (any): Parameters passed to callback. May be null.
        """        
        unreal.log("onIndividualJobFinishedCallback")
        global sTime
        eTime = time.time()
        dTime = eTime - sTime
        print("TIME: {}".format(dTime))

    def OnQueueFinishedCallback(self, pipeline_executor: any, result: bool) -> None:
        """
        Callback delegate called after whole queue finish.
        Prints final state of executor into Unreal Engine Output Log.

        Args:
            pipeline_executor (any): Parameter passed to callback. May be null.
            result (bool): Result of queue execution.
        """        
        unreal.log("All sequences rendered. State:" + str(result))

    def createRenderQueue(self, sequences: array, map: unreal.SoftObjectPath, preset: unreal.MoviePipelineMasterConfig, dir: str) -> None:
        """
        Populates queue with jobs (sequences) to render.
        Sets preset and output directory for every job.

        Args:
            sequences (array): Array of existing sequences.
            map (unreal.SoftObjectPath): SoftObjectPath to current world.
            preset (unreal.MoviePipelineMasterConfig): Preset to modify.
            dir (str): Global directory to store generated sequences.
        """        
        MPQsubsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem) 
        pipelineQueue = MPQsubsystem.get_queue()
        if len(pipelineQueue.get_jobs()) != 0:
            pipelineQueue.delete_all_jobs()
        jobIter = 0
        for seq in sequences:
            job = pipelineQueue.allocate_new_job(unreal.MoviePipelineExecutorJob)
            job.map = map
            job.job_name = "Camera" + str(jobIter)
            job.sequence = unreal.SoftObjectPath(seq.get_path_name())
            jobDir = dir + "\\" + str(job.job_name)
            modPreset = self.modifyJobPreset(preset, jobDir)
            job.set_configuration(modPreset)
            jobIter += 1
            job.get_configuration().initialize_transient_settings()
        
    def executeRenderQueue(self) -> None:
        """
        Executes existing queue in PIE (Play-In-Editor) mode.
        Calls callbacks after every job and after queue execution.
        Starts counting time to measure duration of execution.
        """        
        MPQsubsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem) 
        global executor
        executor = unreal.MoviePipelinePIEExecutor(MPQsubsystem)
        executor.on_individual_job_work_finished_delegate.add_callable_unique(self.OnIndividualJobFinishedCallback)
        executor.on_executor_finished_delegate.add_callable_unique(self.OnQueueFinishedCallback)
        global sTime
        sTime = time.time()
        MPQsubsystem.render_queue_with_executor_instance(executor)

    def pickDirectory(self) -> str:     
        """
        Calls file explorer window to choose directory.
        Returns:
            str: Path to choosen directory.
        """        
        tkinter.Tk().withdraw() 
        return filedialog.askdirectory()
