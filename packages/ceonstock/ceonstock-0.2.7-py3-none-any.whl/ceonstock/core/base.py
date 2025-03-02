# Provides base classes for proper type hinting
from enum import Enum
from abc import ABC

from ceonstock.errors import CstockUnknownTypeError


class CstockBaseClass(ABC):
    """A base class for all custom Cstock classes to inherit from."""


class CstockBaseEnum(str, Enum):
    """A base class for all custom Cstock types (enums) to inherit from."""

    # TODO test: does change/affect behaviour if the enum type is passed directly a search value?
    # E.g. CstockProjInputType(CstockProjInputType.IMG) instead of passing a string?
    @classmethod
    def _missing_(cls, value: str):
        # Allow this Enum to match string values case-insensitively
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        # If not found, raise a CstockUnknownTypeError instead of the default ValueError
        raise CstockUnknownTypeError(received=value, expected=cls)
