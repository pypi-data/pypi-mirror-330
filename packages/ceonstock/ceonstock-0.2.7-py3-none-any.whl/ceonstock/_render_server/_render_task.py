from typing import List, Dict
from uuid import uuid4, UUID
from dataclasses import dataclass, field

from . import render_task_type
from . import base as cbase
from ..log import create_new_logger

logger = create_new_logger(__name__)
logger.setLevel("DEBUG")


@dataclass
class CstockRenderTask(cbase.ICstockPipelineData):
    task_name: str
    app: render_task_type.CstockRenderAppType
    app_version: str
    app_project_folder: str
    target_file: str
    app_render_settings: render_task_type.ICstockRenderAppSettings
    output: str
    dependencies: List[str] = field(default_factory=list)
    task_uuid: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if self.dependencies == None:
            self.dependencies = []
        if not self.task_uuid:
            self.task_uuid = uuid4()


# A collection of tasks that must be completed to conclude the job.
@dataclass
class CstockRenderPipeline():
    render_tasks: List[CstockRenderTask]
    outputs: Dict[str, List[str]]

