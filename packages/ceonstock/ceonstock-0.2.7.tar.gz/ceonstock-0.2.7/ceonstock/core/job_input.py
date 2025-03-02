from __future__ import annotations
import logging
from typing import List, Optional, ClassVar, Type
from dataclasses import dataclass, field

import ceonstock.errors as errors
from ceonstock.core.base import CstockBaseClass, CstockBaseEnum
from ceonstock.core import validator
from ceonstock.log.diagnostics import init_args

# Don't use StrEnum  until Houdini and all other apps are updated to Python 3.11
# from enum import StrEnum, auto
from enum import Enum

logger = logging.getLogger(__name__)


# Inherting from str makes the enum JSON serializable
class CstockJobInputType(str, Enum):
    AUDIO = "audio"
    BOOL = "bool"
    COLOR = "color"
    FLOAT = "float"
    IMG = "img"
    INT = "int"
    STRING = "string"


FILE_TYPES = [CstockJobInputType.AUDIO, CstockJobInputType.IMG]


@dataclass
class CstockJobInput(CstockBaseClass):
    """Represents a single Job Input."""

    #  Make types easily accessible for user without needing to explicitly import CstockJobInputType
    types: ClassVar[Type[CstockJobInputType]] = CstockJobInputType

    name: str
    job_input_type: CstockJobInputType
    values: List = field(default_factory=list)
    # Computed field but cannot use init=False becasue it causes an error when loading from json import.
    is_file_type: bool = False

    def __post_init__(self):
        logger.debug(
            f"Instantiating {self.__class__.__name__} with __init__ locals: {init_args()}"
        )
        self.job_input_type = validator.enforce_enum(
            self.job_input_type, CstockJobInputType
        )
        self.is_file_type = self.job_input_type in FILE_TYPES
        self.validate()
        logger.debug(f"Initialized {self}")

    def __str__(self):
        msg = f"<{self.__class__.__name__}({self.job_input_type}) '{self.name}': {self.values}>"
        return msg

    def __repr__(self):
        return self.__str__()

    def validate(self):
        """Performs validation, collecting errors so that they can all be reported together"""
        logger.debug(f"Validating {self.__class__.__name__} '{self.name}'...")
        validation_errors = []
        if not isinstance(self.values, list):
            validation_errors.append(
                f"{self.__class__.__name__}.values expects a list but received type: {type(self.values)}"
            )

        # Raise errors
        if validation_errors:
            raise errors.CstockInstantiationError(
                cstock_cls=self.__class__, errors=validation_errors
            )
        logger.debug(f"... Validated {self}")
