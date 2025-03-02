from enum import Enum
from typing import Dict
from dataclasses import dataclass

from ..core.base import ICstockPipelineData


class ActionType(str, Enum):
    IMGS_FROM_DOC = "imgs_from_doc"
    IMG_CROP = "img_crop"
    IMG_RESIZE = "img_resize"
    COL_HEX_TO_RGB = "col_hex_to_rgb"  # TODO Move non-file actions elswhere?


@dataclass
class SubmissionAction(ICstockPipelineData):
    action_type: ActionType
    action_args: Dict

    @classmethod
    def from_dict(cls, dict_data):
        args = {
            "action_type": dict_data["action_type"],
            "action_args": dict_data.get("action_args", {}),
        }
        return cls(**args)

    def to_dict(self):
        new_dict = {
            "action_type": self.action_type.value,
            "action_args": self.action_args,
        }
        return new_dict
