import logging
import math
from typing import Optional
from datetime import timedelta
from dataclasses import dataclass
from typing import Union
from pathlib import Path

from ceonstock import config
from ceonstock import CstockJob
from ceonstock import CstockJobInput

logger = logging.getLogger(__name__)


# TODO move vtt file to cstock filesystem module
@dataclass
class VTTFileCue:
    """A single 'entry' in a VTT file"""

    identifier: str
    start_time_seconds: float
    end_time_seconds: float
    content: str

    def apply_time_offset(self, time_seconds: float):
        self.start_time_seconds += time_seconds
        self.end_time_seconds += time_seconds

    def __str__(self):
        return (
            f"{self.identifier}\n"
            f"{seconds_to_timestamp(self.start_time_seconds)}"
            f" --> {seconds_to_timestamp(self.end_time_seconds)}\n"
            f"{self.content}"
        )


class VTTFileProjectInputExample:
    def __init__(
        self,
        file_path: Union[Path, str],
        project_input_name: str,
        file_description: str = "",
    ):
        """
        start_frame: The frame number that corresponds to time 0.00 in the video.
        """
        self.file_path = Path(file_path)
        self.project_input_name = project_input_name
        if not file_description:
            file_description = (
                f"Ceonstock project input examples: {self.project_input_name}"
            )
        self.file_description = file_description
        self._cues: list[VTTFileCue] = []

    def save(
        self,
        ceonstock_jobs: list[CstockJob],
        project_video_length_seconds: Optional[float] = None,
        project_start_frame: Optional[int] = None,
    ) -> Path:
        """Generate the vtt file for the provided ceonstock_jobs."""
        # cues = self._create_cues_for_cstock_jobs(ceonstock_jobs)
        if not project_start_frame:
            logger.warning(
                "Did not receive project_start_frame argument. Getting minimum value from job_limits"
            )
            job_start_frames = [
                int(ceonstock_job.limit_frames.split(" ")[0])
                for ceonstock_job in ceonstock_jobs
                if ceonstock_job.limit_frames
            ]
            lowest_frame = min(job_start_frames)
            project_start_frame = lowest_frame
            logger.warning(f"{project_start_frame=}")
            # project_start_frame = #TODO get min frame.

        cues = [
            self._create_cue_for_cstock_job(
                job, str(i), start_frame=project_start_frame
            )
            for i, job in enumerate(ceonstock_jobs)
        ]
        logger.debug(f"Created cues: {cues}")
        for cue in cues:
            logger.debug(cue)
        offset_overlapping_cues(cues, project_video_length_seconds)
        logger.debug(f"Updated? cues: {cues}")
        for cue in cues:
            logger.debug(cue)
        self._cues = cues
        file_content = self._file_content()
        if not self.file_path.parent.exists():
            logger.info(f"Creating dir: {self.file_path.parent}")
            self.file_path.parent.mkdir(exist_ok=True, parents=True)
        logger.info(f"Saving file: {self.file_path}")
        with open(self.file_path, "w") as f:  #
            f.write(file_content)
        return Path(self.file_path)

    def _create_cue_for_cstock_job(
        self,
        ceonstock_job: CstockJob,
        cue_identifier: str,
        fps=config.DEFAULT_FPS,
        start_frame: int = 0,
    ) -> VTTFileCue:
        """
        start_frame: The frame which corresponds to time 0.0 in the video.
        """
        cue_identifier = str(cue_identifier)
        if not ceonstock_job.limit_frames:
            raise Exception(
                "VTT file received a ceonstock job which does not have limit_frames set."
            )
        # TODO refactor limit_frames (and cstock workflow as a whole) to accept
        # time ranges instead of frames?
        job_start_frame = int(ceonstock_job.limit_frames.split(" ")[0])
        job_end_frame = int(ceonstock_job.limit_frames.split(" ")[1])
        start_time = (job_start_frame - start_frame) / fps
        end_time = (job_end_frame - start_frame + 1) / fps
        # Add +1 to the end frame so that the end time represents the END of the frame.
        # For example, first frames starts at time 0.0 but will show onscreen for 1/fps seconds.
        # To make the time ranges fully encompass the frame range, we need to capture the END of the end
        # frame. This also causes the cue timings to be joined end-to-start of next cue.
        target_job_input: Optional[CstockJobInput] = None
        for job_input in ceonstock_job.job_inputs:
            if job_input.name == self.project_input_name:
                target_job_input = job_input
                break
        if not target_job_input:
            raise Exception(
                f"Could not find job_input with project_input_name '{self.project_input_name}'"
            )
        values = [str(value) for value in target_job_input.values]
        content = "\n".join(values)
        cue = VTTFileCue(
            identifier=str(cue_identifier),
            start_time_seconds=start_time,
            end_time_seconds=end_time,
            content=content,
        )
        return cue

    def cues(self):
        return self._cues

    def _header(self) -> str:
        vtt_header = "WEBVTT"  # Required start of file string for VTT files.
        if self.file_description:
            if "-->" not in self.file_description:
                vtt_header += f" {self.file_description}"
            else:
                logger.warning(
                    "File description contains invalid content '-->', it will not be added to the vtt file."
                )
        return vtt_header

    def _file_content(self) -> str:
        """Return the string representing the full VTT file"""
        logger.debug(f"Formatting VTT content")
        vtt_data_body = "\n\n".join([str(cue) for cue in self.cues()])
        vtt_data = self._header() + "\n\n" + vtt_data_body
        return vtt_data


def offset_overlapping_cues(
    cues: list[VTTFileCue],
    project_video_length_seconds: Optional[float] = None,
):
    """
    When we loop/repeat a cstock project video with varying example inputs, the generated job frameranges
    fall out of sync with the total video length.
    If we find a timestamp that overlaps with a previous timestimp, push it to the next 'video cycle'
    """
    # NOTE: This logic assumes that cues are indexed in order of appearance in the video
    if not cues:
        logger.warning(
            "Could not apply video cycling to vtt timestamps: No cues received."
        )
        return cues

    if not project_video_length_seconds:
        logger.warning(
            f"Did not receive explicit declaration of project length. Assuming latest found cue end time as"
            "the project length. This may cause desync if cues were not created for the full video length."
        )
        max_cue_time = max(
            cues, key=lambda x: x.end_time_seconds
        ).end_time_seconds
        logger.debug(f"{max_cue_time=}")
        project_video_length_seconds = max_cue_time
        logger.debug(
            f"Assuming video length from existing cues: {project_video_length_seconds=}"
        )

    def _relative_time(time_seconds: float) -> float:
        """Return the time relative to the current loop"""
        if time_seconds == 0:
            return 0  # 0 is always the START of a loop.

        relative_time = time_seconds % project_video_length_seconds
        if relative_time == 0:
            # Since we already handled the 0 case, we can assume we are at the END of the loop.
            return project_video_length_seconds
        return relative_time

    previous_cues_max_end_time = 0.0
    for cue in cues:
        logger.debug(f"{previous_cues_max_end_time=}")
        if cue.start_time_seconds >= previous_cues_max_end_time:
            # The cues are progressing in normal expected order
            previous_cues_max_end_time = max(
                previous_cues_max_end_time, cue.end_time_seconds
            )
            logger.debug(f"cue({cue.identifier}) does not need shifting.")
            continue

        # This cue is starting earlier than a previous cue
        # Determine if we need move to the next loop or append the cue to the current loop
        relative_start_time = _relative_time(cue.start_time_seconds)
        previous_cues_max_end_time_relative = _relative_time(
            previous_cues_max_end_time
        )
        logger.debug(f"{relative_start_time=}")
        logger.debug(f"{previous_cues_max_end_time_relative=}")
        current_loop = _calculate_loop_num_for_time(
            previous_cues_max_end_time, project_video_length_seconds
        )
        logger.debug(f"{current_loop=}")
        if relative_start_time >= previous_cues_max_end_time_relative:
            target_loop = current_loop
        else:
            target_loop = current_loop + 1
        logger.debug(f"{target_loop=}")

        set_cue_to_loop_num(cue, target_loop, project_video_length_seconds)
        previous_cues_max_end_time = max(
            previous_cues_max_end_time, cue.end_time_seconds
        )


def seconds_to_timestamp(time_seconds: float) -> str:
    """Return a timestamp formatted for a VTT file"""
    td = timedelta(seconds=time_seconds)
    # Get the hours, minutes, and seconds.
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    # Round the microseconds to millis.
    millis = int(round(td.microseconds / 1000, 0))
    str_timestamp = f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"
    return str_timestamp


def _calculate_loop_num_for_time(
    time_seconds: float, loop_length_seconds: float
) -> int:
    """
    Return the loop number based on the provided time.
    0 represents the videos first playthrough
    1 represents the first repeat of the video
    """
    loop_num = math.floor(time_seconds / loop_length_seconds)
    if time_seconds % loop_length_seconds == 0:
        # Special case in which the cue ends exactly at the end time of the project
        return loop_num - 1
    return loop_num


def set_cue_to_loop_num(
    cue: VTTFileCue, loop_num: int, loop_length_seconds: float
):
    """
    Loop num 0 is the first video playthrough.
    Loop num 1 is the first repeat of the video.
    """
    # In case the timestamp was already outside of the project length, use the remainder
    # to calcualte the relative start time.
    time_seconds = cue.start_time_seconds
    relative_start_time = time_seconds % loop_length_seconds
    loop_num_start_time_seconds = loop_length_seconds * loop_num
    new_start_time = loop_num_start_time_seconds + relative_start_time
    offset_amount = new_start_time - time_seconds

    # Apply offset to cue
    logger.debug(
        f"Current cue time: {cue.start_time_seconds} -> {cue.end_time_seconds})"
    )
    cue.apply_time_offset(offset_amount)
    logger.debug(
        f"Updated cue time: {cue.start_time_seconds} -> {cue.end_time_seconds})"
    )
    logger.debug(
        f"Pushed cue({cue.identifier}) to video cyle {loop_num}: {cue.start_time_seconds} -> {cue.end_time_seconds}"
    )
