from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import ClassVar, Type, Any, List, Dict
from typing import Optional, Union
from typing import TypedDict

from . import CstockProjectInput
from .base import CstockBaseClass
from .file_action import CstockFileAction

logger = logging.getLogger(__name__)


# class CropSettings(TypedDict):
#     x: float
#     y: float
#     width: float
#     height: float


@dataclass
class CstockSubmissionInputRaw:
    """
    Raw inputs represent the files/values as directly received from the web-client.
    Some files may need to be pre-processed e.g. convert a word document to a set of images.
    """

    values: List
    project_input: CstockProjectInput
    preprocess_actions: List[CstockFileAction] = field(default_factory=list)

    def __post_init__(self):
        # Enforce loading of types when loaded from a dict (imported json)
        if not isinstance(self.project_input, CstockProjectInput):
            self.project_input = CstockProjectInput(**self.project_input)

        def enforce_file_action(file_action) -> CstockFileAction:
            if isinstance(file_action, CstockFileAction):
                return file_action
            # If it's not a CstockFileAction, assume it's a dict and try to load
            return CstockFileAction(**file_action)

        self.preprocess_actions = [
            enforce_file_action(file_action)
            for file_action in self.preprocess_actions
        ]

    def __str__(self):
        return f"<{self.__class__.__name__} for '{self.project_input.name}': {self.values}>"


@dataclass
class CstockSubmissionInputEntry(CstockBaseClass):
    value: Any
    entry_actions: List[CstockFileAction]

    def __post_init__(self):
        # Enforce class isntances when loaded from a dict
        def enforce_instance(
            entry_action: Union[dict, CstockFileAction]
        ) -> CstockFileAction:
            if isinstance(entry_action, CstockFileAction):
                return entry_action
            return CstockFileAction(**entry_action)

        self.entry_actions = [
            enforce_instance(action) for action in self.entry_actions
        ]


@dataclass
class CstockSubmissionInput(CstockBaseClass):
    """Represents a single submission for a project input.
    A single submission can contain multiple entries.
    Each entry may contain extra data depending on its type.
    For example, images can optionally contain information about how to crop them.
    """

    entries: List[CstockSubmissionInputEntry]
    project_input: CstockProjectInput

    def __post_init__(self):
        # Handle loading from json/serializable dict.
        if isinstance(self.project_input, dict):
            self.project_input = CstockProjectInput(**self.project_input)

        def enforce_instance(
            entry: Union[Dict, CstockSubmissionInputEntry]
        ) -> CstockSubmissionInputEntry:
            if isinstance(entry, CstockSubmissionInputEntry):
                return entry
            return CstockSubmissionInputEntry(**entry)

        self.entries = [enforce_instance(entry) for entry in self.entries]

    def __str__(self):
        msg = f"<{self.__class__.__name__} '{self.project_input.name}': {len(self.entries)} entries>"
        return msg
