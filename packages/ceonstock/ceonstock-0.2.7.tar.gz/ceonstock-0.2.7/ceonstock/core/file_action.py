from dataclasses import dataclass, field
from typing import Callable, ClassVar, TypeVar
from typing import Union
from typing import Dict
from abc import ABC
from ceonstock.core.base import CstockBaseEnum
from ceonstock.core.base import CstockBaseClass


class CstockFileActionType(CstockBaseEnum):
    DOC_TO_IMGS = "doc_to_imgs"
    RESIZE = "resize"
    CROP = "crop"


# All file action kwargs inherit from this base class.
# These are used to validate the file action kwargs according to the type.
class CstockFileActionKwargs(ABC):
    pass


# The CstockFileAction class is to be used for storing file actions, converting to/from json.
@dataclass
class CstockFileAction(CstockBaseClass):
    action_type: Union[str, CstockFileActionType]
    action_kwargs: Union[Dict, CstockFileActionKwargs]

    def __str__(self):
        return f"<{self.__class__.__name__} {self.action_type}: {self.action_kwargs}>"

    def __post_init__(self):
        """Validate kwargs"""
        # Enforce enum type
        if not isinstance(self.action_type, CstockFileActionType):
            self.action_type = CstockFileActionType(self.action_type)
        # Enforce kwargs type
        loadable_classes = [
            CstockFileActionCrop,
            CstockFileActionResize,
            CstockFileActionDocToImgs,
        ]
        kwargs_lookup = {
            file_action.action_type: file_action
            for file_action in loadable_classes
        }
        if not isinstance(self.action_kwargs, CstockFileActionKwargs):
            cls_to_load = kwargs_lookup[self.action_type]
            loaded_cls = cls_to_load(**self.action_kwargs)
            self.action_kwargs = loaded_cls


@dataclass
class CstockFileActionCrop(CstockFileActionKwargs):
    action_type: ClassVar[CstockFileActionType] = CstockFileActionType.CROP
    # Crop settings handled as PERCENTAGES.
    x: float
    y: float
    width: float
    height: float


@dataclass
class CstockFileActionResize(CstockFileActionKwargs):
    action_type: ClassVar[CstockFileActionType] = CstockFileActionType.RESIZE
    max_width: int
    max_height: int


# For types that don't accept any arguments
@dataclass
class CstockFileActionDocToImgs(CstockFileActionKwargs):
    action_type: ClassVar[
        CstockFileActionType
    ] = CstockFileActionType.DOC_TO_IMGS


# def get_kwargs(
#     file_action_type: CstockFileActionType,
# ) -> CstockFileActionKwargs:
