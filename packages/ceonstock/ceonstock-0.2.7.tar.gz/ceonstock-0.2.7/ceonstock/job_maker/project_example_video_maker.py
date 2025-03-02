import logging
import math
from dataclasses import dataclass
from typing import Union, Dict
from typing import Optional
from uuid import uuid4
from copy import deepcopy
from pathlib import Path

from ceonstock import config as ceonstock_config
from ceonstock import CstockProject
from ceonstock import CstockProjectInput

# from ceonstock import CstockRenderTask
# from ceonstock import CstockRenderAppType
from ceonstock import CstockJob
from ceonstock import CstockJobInput

# from ceonstock.core.render_task import CstockRenderTaskAppSettingsHou
from ceonstock.job_maker import CstockJobGenerator

from ceon_render import AppRenderJob, CeonRenderJobSettings
from ceon_render import CeonRenderPipelineJob
from ceon_render import render_apps
from ceon_render import render_pipeline as crp

from app.job_manager.job_manager import JobManager

logger = logging.getLogger(__name__)


@dataclass
class Frames:
    start: int
    end: int
    increment: int = 1

    @classmethod
    def from_string(cls, frames_str: str):
        frames_list = frames_str.split(" ")
        valid_lengths = [2, 3]
        if len(frames_list) not in valid_lengths:
            raise Exception(
                f"Invalid length '{len(frames_list)}' after splitting string {frames_str}"
            )
        start = int(frames_list[0])
        end = int(frames_list[1])
        if len(frames_list) == 3:
            increment = int(frames_list[2])
            return Frames(start=start, end=end, increment=increment)
        else:  # Increment is not present in the string
            return Frames(start=start, end=end)

    def num_frames(self) -> int:
        return (self.end - self.start) + 1

    def __post_init__(self):
        self.start = int(self.start)
        self.end = int(self.end)
        self.increment = int(self.increment)
        if self.start > self.end:
            raise Exception("Start frame cannot be great than end frame")


def _get_frames_for_project(ceonstock_project: CstockProject):
    """Take the min/max between all render tasks"""

    def _get_frames_for_task(
        ceon_render_job: CeonRenderPipelineJob,
    ) -> Optional[Frames]:
        """Get frames for each task. Return None for tasks that do not have frames"""
        file_dirs = {"project": "TODOsetprojectpathfor _get_frames_for_task"}
        app_type = ceon_render_job.app_type
        # CeonRenderJobSettings(frame_dimension=())
        if app_type.lower() == "hou":
            # app_job: render_apps.AppRenderJobHou = (
            #     crp.pipeline_job_to_concrete_job(
            #         ceonstock_project.render_pipeline,
            #         ceon_render_job,
            #         file_reference_dirs=file_dirs,
            #         render_settings=render_job_settings
            #     )
            # )
            # app_render_settings = ceon_render_job.app_render_settings
            # frames_str = app_render_settings.frames
            hou_frames = ceon_render_job.app_render_settings["frames"]
            # TODO remove string frame format, use tuples instead.
            # Currently converting for backwards compatibility. Can probably remove Frames class.
            # frames_str = f"{hou_frames[0]} {frames[1]}"
            logger.info("Got frames for hou task in _get_frames_for_task.")
            return Frames.from_string(hou_frames)
        if app_type.lower() == "ffmpeg":
            logger.warning(
                "Could not determine frames for ffmpeg task (not implemented). Returning None"
            )
            return None
        raise Exception(f"Could not determine frames for app_type: {app_type}")

    # render_settings = job_manager._create_render_settings_for_job()
    all_task_frames = [
        _get_frames_for_task(render_task)
        for render_task in ceonstock_project.render_pipeline.pipeline_jobs
    ]
    valid_task_frames = [
        task_frames for task_frames in all_task_frames if task_frames != None
    ]

    min_frame = min([frames.start for frames in valid_task_frames])
    max_frame = max([frames.end for frames in valid_task_frames])
    project_frames = Frames(start=min_frame, end=max_frame)
    return project_frames


def _get_num_entries_for_current_job(
    i: int, *, min_entries: int, max_entries: int
) -> int:
    """
    Logic to determine the number of entries to include in the job.
    i: represents the current job number within this particular job batch.
    For example, if we are generating 3 example jobs (for the same project_input), i will range from 0-2
    """
    diff = abs(max_entries - min_entries)
    middle_entries = math.floor(min_entries + (diff / 2))
    logger.debug(f"Got num_entries middle value: {middle_entries=}")
    desired = [min_entries, middle_entries, max_entries]
    default = middle_entries
    try:
        return desired[i]
    except IndexError:
        return default


def _get_desired_num_examples(project_input: CstockProjectInput):
    default = 3  # For cases that are TODO
    if project_input.web_input_type == project_input.web_input_types.DROPDOWN:
        num_dropdown_options = len(_list_dropdown_values(project_input))
        logger.debug(f"Detected {num_dropdown_options=}")
        return num_dropdown_options

    if project_input.job_input_type == project_input.job_input_types.BOOL:
        # Currently assumes one bool value. TODO handle multiple values elegantly
        # Ideal setup:
        #     All off
        #     All on
        #     Alternate 10
        #     Alternate 01
        return 2
    logger.warning(
        "TODO: Get number of generation dynamically (currently defaults to 3 for non dropdown/bools)"
    )
    # Probably want to infer based on number of 'filesets' in the input files directory.
    # E.g. admin can make folders:
    #      ImgColorTest
    #         - imgColorDemo.jpg
    #      ImgPhotos
    #         - photo1.jpg
    #         - photo2.jpg
    #         - photo3.jpg
    #      ImgDigitalArtwork
    #         - photo1.jpg
    #         - photo2.jpg
    #         - photo3.jpg
    # This would generate three examples, where each one sources from the relevant image set.
    return default


def create_jobs_for_project_input_example_video(
    ceonstock_project: CstockProject,
    *,
    project_input_name: str,
    baseline_job: CstockJob,
    job_generator: CstockJobGenerator,
) -> list[CstockJob]:
    """
    Takes a baseline job and generates various variations with different values for the target project_input_name
    job_generator: Handles the value selection logic to generate the new jobs.
    """
    # Setup
    logger.info(
        f"\nCreating jobs for project_input '{project_input_name}' example video."
    )

    target_project_input = None
    for project_input in ceonstock_project.project_inputs:
        if project_input.name == project_input_name:
            target_project_input = project_input
    if not target_project_input:
        raise Exception(f"Could not find project input named {project_input_name}")

    new_jobs = []
    num_examples_to_generate = _get_desired_num_examples(target_project_input)
    for i in range(num_examples_to_generate):
        num_entries = _get_num_entries_for_current_job(
            i,
            min_entries=target_project_input.num_entries_min,
            max_entries=target_project_input.num_entries_max,
        )
        logger.debug(f"{num_entries=}")
        logger.debug(f"{target_project_input.num_entries_min=}")
        logger.debug(f"{target_project_input.num_entries_max=}")
        new_job_input = job_generator.generate_job_input(
            target_project_input, num_entries=num_entries
        )
        logger.info(f"Created new job input: {new_job_input}")
        baseline_job_copy = create_job_copy_with_new_uuid(baseline_job)
        new_job = _replace_job_input(baseline_job_copy, new_job_input)
        new_jobs.append(new_job)

    # -----
    # Apply/calculate job frame limits
    # ----
    # Setup rendering for only a portion of the frame range.
    # Videos will be appended together.
    # TODO proper fps workflow instead of assumption
    min_job_frame_length = ceonstock_config.DEFAULT_FPS * 2
    project_frames = _get_frames_for_project(ceonstock_project)
    # Ideally, we show all examples with one pass of the video
    num_video_repeats = _calculate_required_number_of_video_repeats(
        num_jobs=len(new_jobs),
        min_job_frame_length=min_job_frame_length,
        num_project_frames=project_frames.num_frames(),
    )
    num_video_cycles = num_video_repeats + 1
    if num_video_repeats == 0:
        _split_job_frame_limits(new_jobs, project_frames)
        return new_jobs
    logger.info(
        f"Preparing frame ranges for {len(new_jobs)} jobs, spread over {num_video_cycles} video cycles"
    )
    num_jobs_per_video_cycle = math.ceil(len(new_jobs) / num_video_cycles)
    for i in range(num_video_cycles):
        start_index = num_jobs_per_video_cycle * i
        logger.debug(f"{start_index=}")
        end_index = start_index + num_jobs_per_video_cycle
        end_index = min(end_index, len(new_jobs))
        logger.debug(f"{end_index=}")
        jobs_for_cycle = new_jobs[start_index:end_index]
        logger.debug(f"{jobs_for_cycle=}")
        _split_job_frame_limits(jobs_for_cycle, project_frames)
    return new_jobs


def _split_job_frame_limits(jobs: list[CstockJob], project_frames: Frames):
    """Equally divide the available project frames among the received jobs.
    Modifies the jobs in place"""
    if not len(jobs) >= 1:
        logger.warning("Received EMPTY job of lists. No frame ranges were set.")
        return
    num_project_frames = project_frames.num_frames()
    frames_per_segment: int = math.floor(num_project_frames / len(jobs))
    logger.debug(f"Got project frames: {num_project_frames}")
    logger.debug(f"Setting job frame limits...")
    logger.debug(f"Frames per segment: {frames_per_segment}")
    logger.warning(
        "TODO: Handle missing frame in final job segment when num frames is odd."
    )
    for i, job in enumerate(jobs):
        logger.debug(
            f"job[{i}]({job.job_uuid:.5}) limit_frames: {jobs[i].limit_frames}"
        )
        frame_offset = i * frames_per_segment
        start = project_frames.start + frame_offset
        end = start + (frames_per_segment - 1)
        job.limit_frames = f"{start} {end}"
        logger.debug(
            f"job[{i}]({job.job_uuid:.5}) frame update: {jobs[i].limit_frames}"
        )


def _calculate_required_number_of_video_repeats(
    *, num_jobs: int, min_job_frame_length: int, num_project_frames: int
) -> int:
    required_total_frames = min_job_frame_length * num_jobs
    if required_total_frames <= num_project_frames:
        return 0
    num_repeats_for_all_jobs = math.floor(required_total_frames / num_project_frames)
    logger.debug(
        f"Calculated required number of video repeats for {num_jobs} jobs: {num_repeats_for_all_jobs}"
        f"\n{num_project_frames=}"
        f"\n{min_job_frame_length=}"
    )
    return num_repeats_for_all_jobs


def create_job_copy_with_new_uuid(cstock_job: CstockJob):
    """Create a copy of the current job with a new uuid"""
    job = deepcopy(cstock_job)
    job.job_uuid = str(uuid4())
    return job


def _replace_job_input(
    cstock_job: CstockJob, new_job_input: CstockJobInput
) -> CstockJob:
    """
    Replace a job input in a cstock job.
    Returns a copy.
    """
    job = deepcopy(cstock_job)
    for i, job_input in enumerate(job.job_inputs):
        if job_input.name != new_job_input.name:
            continue
        job.job_inputs[i] = new_job_input
        return job
    # The job_input name was not found
    raise Exception(
        f"Failed to replace job_input: job does not contain an input with matching name '{new_job_input.name}'."
    )


def _list_dropdown_values(project_input: CstockProjectInput) -> list:
    """
    Extract the dropdown options from the project input and return the values as a list
    """
    if not project_input.web_input_type == project_input.web_input_types.DROPDOWN:
        raise Exception(
            f"Cannot get dropdown options: Received project_input {project_input.name} is not a DROPDOWN web_input_type."
        )
    dropdown_options = project_input.type_settings["dropdown_options"]
    values = [option["value"] for option in dropdown_options]
    logger.debug(f"Got valid dropdown option values: {values}")
    return values
