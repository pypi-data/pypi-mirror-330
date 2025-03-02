import logging
import inspect
from typing import List, Optional, Type
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ceon_render import CeonRenderPipeline

from .base import CstockBaseClass

# from .render import CstockRenderPipeline
from .project_input import CstockProjectInput
from . import validator

# from .render import CstockRenderPipeline

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class CstockProjectInfo(CstockBaseClass):
    """
    Information about this project that is only needed for the website.
    """

    title: str
    description: str = ""
    tags: Optional[List[str]] = field(default_factory=list)


@dataclass(kw_only=True)
class CstockProject(CstockBaseClass):
    """Fundamental data for a Cstock project to function."""

    project_inputs: List[CstockProjectInput]
    render_pipeline: CeonRenderPipeline
    project_info: Optional[CstockProjectInfo] = None
    project_uuid: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        self.project_inputs = validator.enforce_list_of_instances(
            self.project_inputs, CstockProjectInput
        )
        if self.project_info:
            self.project_info = validator.enforce_class_instance(
                self.project_info, CstockProjectInfo
            )
        self.project_uuid = str(self.project_uuid)
        self.render_pipeline = validator.enforce_class_instance(
            self.render_pipeline, CeonRenderPipeline
        )

    def project_input(self, project_input_name: str) -> CstockProjectInput:
        """Fetch a project input by name"""
        target_input = None
        for project_input in self.project_inputs:
            if project_input.name == project_input_name:
                target_input = project_input
                break
        if not target_input:
            raise Exception(
                f"Could not find target project_input: {project_input_name}"
            )
        return target_input

    def validate(self):
        if not isinstance(self.project_inputs, list):
            raise Exception(
                f"CstockProject project_inputs is not a list: {self.project_inputs}"
            )
        for project_input in self.project_inputs:
            if not isinstance(project_input, CstockProjectInput):
                raise Exception(
                    f"CstockProject contains a project_input which is not an instantiated cstock instance: {project_input}"
                )
        if not isinstance(self.render_pipeline, CeonRenderPipeline):
            raise Exception(
                f"CstockProject contains a render_pipeline which is not a cstock instance: {self.render_pipeline}"
            )
        if not isinstance(self.project_info, CstockProjectInfo):
            raise Exception(
                f"CstockProject contains project_info which is not a cstock instance: {self.project_info}"
            )
        if not isinstance(self.project_uuid, str):
            raise Exception(
                f"CstockProject project_uuid is not a str instance: {self.project_uuid}"
            )
