from dataclasses import dataclass
from typing import List, Dict, Optional
from copy import deepcopy

from ..core import proj_input_type as cprojtype
from ..core import job_input_type as cjobtype
from ..core.proj_input import CstockProjInputGroup
from ..log import create_new_logger
from ..utils import printify
from ..core.base import ICstockPipelineData
from ..version import VERSION
from .actions import SubmissionAction

logger = create_new_logger(__name__)

# TODO use these? NOt currently used


@dataclass
class CstockSubmissionInputEntry(ICstockPipelineData):
    value: str
    actions: List[SubmissionAction]

    @classmethod
    def from_dict(cls, dict_data):
        logger.debug(f"<{cls.__name__}>.from_dict got dict_data: {printify(dict_data)}")
        args = {
            "value": dict_data["value"],
            "actions": [
                SubmissionAction.from_dict(process_action)
                for process_action in dict_data["actions"]
            ],
        }
        logger.debug(f"<{cls.__name__}>.from_dict created args: {args}")
        return cls(**args)

    def to_dict(self):
        new_dict = {
            "value": self.value,
            "actions": [action.to_dict() for action in self.actions],
        }
        return new_dict


@dataclass
class CstockSubmissionInput:
    """The submission entries related to a single CstockProjInput"""

    name: str
    entries: List[CstockSubmissionInputEntry]
    proj_input_type: cprojtype.CstockProjInputType

    @classmethod
    def from_dict(cls, dict_data):
        args = {
            "name": dict_data["name"],
            "entries": [
                CstockSubmissionInputEntry.from_dict(submission_entry)
                for submission_entry in dict_data["entries"]
            ],
        }
        if dict_data.get("proj_input_type"):
            args["proj_input_type"] = cprojtype.CstockProjInputType(
                dict_data["proj_input_type"]
            )
        return cls(**args)

    def to_dict(self):
        new_dict = {
            "name": self.name,
            "entries": [
                submission_entry.to_dict() for submission_entry in self.entries
            ],
        }
        if self.proj_input_type:
            new_dict["proj_input_type"] = self.proj_input_type.value
        return new_dict

    @property  # for parity with access style of proj_input_type
    def job_input_type(self) -> cjobtype.CstockJobInputType:
        # TODO refactor job_input_type to use a type_info class, same format as proj_input_type
        return self.proj_input_type.info().job_input_type

    def values(self):
        return [entry.value for entry in self.entries]

    def remove_actions(self):
        for entry in self.entries:
            entry.actions = []


class CstockSubmissionInputGroup(ICstockPipelineData):
    """Works with a set of SubmissionInputs"""

    def __init__(self, submission_inputs: List[CstockSubmissionInput]):
        self._submission_inputs = submission_inputs

    def __str__(self):
        msg = f"<{type(self).__name__}>"
        return msg

    @classmethod
    def from_raw_entries(
        cls,
        proj_input_group: CstockProjInputGroup,
        user_entries_raw: Dict[str, List[str]],
    ):
        submission_inputs_list = []
        for proj_input in proj_input_group.proj_inputs():
            default_preprocess_actions = proj_input.type().info().preprocess_actions
            logger.debug(f"default_preproces_actions: {default_preprocess_actions}")
            current_input_entries = user_entries_raw[proj_input.name]
            logger.debug(f"current_input_entries: {current_input_entries}")
            user_input_entries = [
                CstockSubmissionInputEntry(entry, default_preprocess_actions)
                for entry in current_input_entries
            ]
            logger.debug(f"Created user_input_entries: {user_input_entries}")
            user_input = CstockSubmissionInput(
                proj_input.name, user_input_entries, proj_input.proj_input_type
            )
            logger.debug(f"Created user_input: {user_input}")
            submission_inputs_list.append(user_input)
        return cls(submission_inputs_list)

    @classmethod
    def from_dict(cls, dict_data):
        submission_inputs = [
            CstockSubmissionInput.from_dict(submission_input)
            for submission_input in dict_data["submission_inputs"]
        ]
        return cls(submission_inputs)

    def to_dict(self):
        """Returns a serializable dict"""
        submission_inputs = dict()
        submission_inputs["submission_inputs"] = [
            submission_input.to_dict() for submission_input in self._submission_inputs
        ]
        submission_inputs["ceonstock_version"] = VERSION

        return submission_inputs

    def submission_inputs(self) -> List[CstockSubmissionInput]:
        return self._submission_inputs
