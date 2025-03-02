import logging
from dataclasses import dataclass, field

# from typing import Dict, List, Optional, ClassVar, Type
# from typing import Union
# from abc import ABC
# from uuid import UUID, uuid4
# from ceonstock import errors

# from .base import CstockBaseClass, CstockBaseEnum
# from .render_task import (
#     CstockRenderAppType,
#     CstockRenderTask,
#     CstockRenderTaskAppSettingsHou,
# )
# from . import validator

logger = logging.getLogger(__name__)


### TODO organize better. Does this belong in ceonstock core module? Better on render server?
@dataclass
class Dimensions:
    """Helper class provides easy lookups for width, height and stringification"""

    width: int
    height: int

    def __post_init__(self):
        self.aspect = self.width / self.height

    def __str__(self):
        return f"{self.width}x{self.height}"


class RenderOutputSettings:
    def __init__(self, width: int, height: int, framerate=30, frames=""):
        self.dimensions = Dimensions(int(width), int(height))
        self.framerate = framerate
        self.frames = frames

    def __str__(self):
        return f"{self.dimensions}, {self.framerate}fps"


# TODO implement extra outputs.
# (Currently unused but useful for e.g. providing a mask for teh flag to the customer)
# @dataclass
# class CstockRenderPipelineExtraOutput:
#     file_source: str # TODO CstockFileReference e.g. from_task, from_project
#     description: str
#     file_rename: Optional[str] = None


# DEPRECATED: Replaced with ceon-render package CeonRenderPipeline.
# @dataclass
# class CstockRenderPipeline(CstockBaseClass):
#     render_tasks: List[CstockRenderTask]
#     output_task: str
#     output_extras: list[str] = field(default_factory=list)
#     # output_extras: list[CstockRenderPipelineExtraOutput] = field(default_factory=list)

#     def __post_init__(self):
#         # When loading from json we may be getting a dict instead of a
#         # class instance.
#         self.render_tasks = validator.enforce_list_of_instances(
#             self.render_tasks, CstockRenderTask
#         )
#         self.output_extras = validator.enforce_list_of_instances(
#             self.output_extras, str
#         )
#         self._validate()

#     def __str__(self):
#         task_names = [
#             render_task.task_name for render_task in self.render_tasks
#         ]
#         msg = f"<{self.__class__.__name__} TASKS:{task_names} OUT:'{self.output_task}')>"
#         return msg

#     def __repr__(self):
#         return self.__str__()

#     def _validate(self):
#         """Ensure that all named tasks exist"""
#         self.get_task(self.output_task)
#         # if self.output_extras:
#         #     for task_name in self.extra_outputs:
#         #         self.get_task(task_name)

#     def get_task(self, task_name: str) -> CstockRenderTask:
#         """Search for a task by it's name.
#         Raises an exception if not found"""
#         for task in self.render_tasks:
#             if task.task_name == task_name:
#                 return task
#         raise ValueError(f"Could not find a task with the name: {task_name}")

#     def primary_output_task(self) -> CstockRenderTask:
#         """
#         Returns the final output file of the pipeline.
#         """
#         final_output_task = self.get_task(self.output_task)
#         return final_output_task

#     def extra_output_tasks(self) -> List[CstockRenderTask]:
#         """
#         Return a list of extra (non-primary) output files created by rendering tasks
#         """
#         if not self.output_extras:
#             return []

#         output_tasks = []
#         for task_name in self.output_extras:
#             task = self.get_task(task_name)
#             output_tasks.append(task)

#         return output_tasks

#     # TODO validate task dependency chain
