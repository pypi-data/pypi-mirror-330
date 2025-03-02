from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import ClassVar, Type

from ceonstock.core.web_input import CstockWebInputType
from ceonstock.core.job_input import CstockJobInputType
from ceonstock.core.base import CstockBaseClass
from ceonstock.core import validator
from ceonstock.log import printify
from ceonstock import errors as cstock_errors

logger = logging.getLogger(__name__)

HARD_LIMIT_NUM_ENTRIES_MAX = 10


@dataclass
class CstockProjectInput(CstockBaseClass):
    """Represents a single Project Input."""

    #  Make types easily accessible for user without needing to explicitly import CstockJobInputType
    job_input_types: ClassVar[Type[CstockJobInputType]] = CstockJobInputType
    web_input_types: ClassVar[Type[CstockWebInputType]] = CstockWebInputType

    name: str
    job_input_type: CstockJobInputType
    web_input_type: CstockWebInputType
    description: str = ""
    type_settings: dict = field(
        default_factory=dict
    )  # User-provided arguments that are unique for this type, e.g. "dropdown_options"
    num_entries_min: int = 1
    num_entries_max: int = 1
    # required: bool = True

    def __post_init__(self):
        # Enforce data types
        self.name = str(self.name)
        self.job_input_type = validator.enforce_enum(
            self.job_input_type, CstockJobInputType
        )
        self.web_input_type = validator.enforce_enum(
            self.web_input_type, CstockWebInputType
        )
        # Validate entries are as expected
        self._validate()

    def _validate(self):
        validation_errors = []
        if not self.name:
            validation_errors.append("'name' is empty")

        # Validate min/max values
        if self.num_entries_max > HARD_LIMIT_NUM_ENTRIES_MAX:
            self.num_entries_max = HARD_LIMIT_NUM_ENTRIES_MAX
            logger.warning(
                f"Clamped num_entrie_max ({self.num_entries_max}) to hard limit: {HARD_LIMIT_NUM_ENTRIES_MAX}"
            )
        if self.num_entries_min < 0:
            logger.warning(
                f"Clamped num_entries_min ({self.num_entries_min}) to 0."
            )
            self.num_entries_min = 0
        if self.num_entries_min > self.num_entries_max:
            validation_errors.append(
                f"num_entries_min: {self.num_entries_min} cannot be greater than num_entries_max: {self.num_entries_max}."
            )

        if validation_errors:
            raise cstock_errors.CstockInstantiationError(
                cstock_cls=CstockProjectInput,
                errors=validation_errors,
            )

    def __str__(self):
        msg = f"<CstockProjInput '{self.name}' of type '{self.job_input_type}' (UI:'{self.web_input_type}')>"
        return msg
