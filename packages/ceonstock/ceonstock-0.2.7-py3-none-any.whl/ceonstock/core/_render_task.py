# DEPRECATED: Replace with ceon-render module.

import logging
from dataclasses import dataclass, field
from typing import ClassVar, Type
from typing import Optional
from abc import ABC
from uuid import UUID, uuid4

from .base import CstockBaseClass, CstockBaseEnum
from .file_reference import CstockFileReference
from . import validator
from ceonstock import errors

logger = logging.getLogger(__name__)


class CstockRenderAppType(CstockBaseEnum):
    HOU = "hou"
    FFMPEG = "ffmpeg"
    NUKE = "nuke"


@dataclass(kw_only=True)
class CstockRenderTaskAppSettings(CstockBaseClass, ABC):
    pass


@dataclass(kw_only=True)
class CstockRenderTask(CstockBaseClass):
    # So that the user can access types without explicitly needing to import CstockRenderAppType
    app_types: ClassVar[Type[CstockRenderAppType]] = CstockRenderAppType

    task_name: str
    app_type: CstockRenderAppType
    app_version: str
    # app_render_settings will be different depending on the app type
    # (e.g. Hou needs a path to a node, FFMPEG takes strings for input/outputs args)
    app_render_settings: CstockRenderTaskAppSettings

    task_input: CstockFileReference  # Input file
    task_output: str  # Output file

    # Store other render tasks which must be completed before this one can start
    task_dependencies: list[str] = field(default_factory=list)
    task_uuid: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.app_type = validator.enforce_enum(
            self.app_type, CstockRenderAppType
        )
        self.task_uuid = validator.enforce_uuid(self.task_uuid)
        self.task_input = validator.enforce_class_instance(
            self.task_input, CstockFileReference
        )

        # Handle dynamic loading of AppSettings class instances
        cls_to_load = APP_SETTINGS_CLS[self.app_type]
        if not isinstance(self.app_render_settings, cls_to_load):
            logger.debug(
                f"Loading app_settings class '{cls_to_load}' from data: {self.app_render_settings}"
            )
            self.app_render_settings = cls_to_load(**self.app_render_settings)
        # except (ValueError, TypeError) as e:
        #     raise errors.CstockInstantiationError(
        #         cstock_cls=self.__class__, errors=[e]
        #     )
        # self.validate()

    # def validate(self):
    #     # Ensure that the correct RenderSettings were provided for the corresponding app type.
    #     expected_cls = APP_SETTINGS_CLS[self.app_type]

    def __str__(self):
        msg = f"<{self.__class__.__name__} '{self.task_name}' ({self.app_type} OUT:'{self.task_output}')>"
        return msg

    def __repr__(self):
        return self.__str__()


@dataclass(kw_only=True)
class CstockRenderTaskAppSettingsFFMPEG(CstockRenderTaskAppSettings):
    app_type: ClassVar[CstockRenderAppType] = CstockRenderAppType.FFMPEG
    input_args: str = ""
    output_args: str = ""


@dataclass(kw_only=True)
class CstockRenderTaskAppSettingsHou(CstockRenderTaskAppSettings):
    app_type: ClassVar[CstockRenderAppType] = CstockRenderAppType.HOU
    target_node: str
    frames: str
    out_dimensions: Optional[str] = None


APP_SETTINGS_CLS = {
    CstockRenderAppType.HOU: CstockRenderTaskAppSettingsHou,
    CstockRenderAppType.FFMPEG: CstockRenderTaskAppSettingsFFMPEG,
}
