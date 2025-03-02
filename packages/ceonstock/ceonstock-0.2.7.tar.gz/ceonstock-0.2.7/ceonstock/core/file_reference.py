from dataclasses import dataclass

from .base import CstockBaseEnum, CstockBaseClass


class CstockFileSourceType(CstockBaseEnum):
    PROJECT = "project"
    JOB_INPUT = "job_input"
    JOB_OUTPUT = "job_output"
    # TASK_INPUT = "task_input"
    TASK_OUTPUT = "task_output"
    ABSOLUTE = "absolute"


@dataclass
class CstockFileReference(CstockBaseClass):
    target: str
    file_source: CstockFileSourceType = CstockFileSourceType.PROJECT
