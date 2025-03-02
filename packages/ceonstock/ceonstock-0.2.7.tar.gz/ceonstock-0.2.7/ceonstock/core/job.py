from dataclasses import dataclass, field
from typing import List, Type, ClassVar
from typing import Optional
from enum import Enum
from uuid import UUID, uuid4

from . import validator
from .job_input import CstockJobInput
from .base import CstockBaseEnum
from .base import CstockBaseClass


class CstockJobType(CstockBaseEnum):
    PREVIEW = "video_preview"  # Deliver a low resolution watermarked sample video.
    VIDEO_HD = "video_hd"  # Deliver a 1920x1080p video.
    VIDEO_4K = "video_4k"  # Deliver a 3840x2160 video.
    # VIDEO_CUSTOM = "video_custom" # future expansion to allow render args to be passed

    # def get_job_settings(self):
    # return get_job_settings(self)


@dataclass
class CstockJob(CstockBaseClass):
    # For easy developer access without needing explicitly import CstockJobType
    job_types: ClassVar[Type[CstockJobType]] = CstockJobType

    job_inputs: List[CstockJobInput]
    project_uuid: str  # Can be looked up if not provided?
    job_type: CstockJobType = CstockJobType.PREVIEW
    job_uuid: str = field(default_factory=lambda: str(uuid4()))
    limit_frames: Optional[str] = None
    # job_settings: args for cusom setups

    def job_input(self, job_input_name: str) -> CstockJobInput:
        """Lookup a job input by name"""
        for job_input in self.job_inputs:
            if job_input.name == job_input_name:
                return job_input
        raise ValueError(f"No job input found for name '{job_input_name}'")

    def __post_init__(self):
        # TODO use 'validator' to enforce enum for proper logging/errors
        self.project_uuid = str(validator.enforce_uuid(self.project_uuid))
        self.job_uuid = str(validator.enforce_uuid(self.job_uuid))
        self.job_type = validator.enforce_enum(self.job_type, CstockJobType)
        self.job_inputs = validator.enforce_list_of_instances(
            self.job_inputs, CstockJobInput
        )
