from __future__ import annotations
from typing import Union, Optional, Type, List, Any, TypeVar

# from ceonstock.core.base import CstockBaseClass, CstockBaseEnum
from ceonstock.log import printify
# Use TypeVar to avoid cyclical imports

if False: # To prevent flake8 from failing on the string type-hints during CI
    from ceonstock.core.base import CstockBaseEnum
    from ceonstock.core.base import CstockBaseClass


class CstockError(Exception):
    """Base class for all Cstock exceptions"""

    pass


class CstockUnknownTypeError(CstockError):
    """Unrecognized value where an enum (or enum-matching string) was expected"""

    def __init__(
        self,
        *,
        received: Any,
        expected: Type["CstockBaseEnum"],
        message: str = "",
    ):
        if not message:
            message = f"Received invalid value for {expected.__name__}: ({type(received)}){received}"
        self.message = message
        super().__init__(self.message)


class CstockInstantiationError(CstockError):
    """Raised when a Cstock class instance could not be instantiated"""

    def __init__(
        self,
        *,
        cstock_cls: Type["CstockBaseClass"],
        errors=[],
        message: str = "",
    ):
        if not message:
            message = f"Failed to instantiate {cstock_cls.__name__}"
        self.message = message
        self.errors = errors
        if self.errors:
            self.message += f": {printify(self.errors)}"
        super().__init__(self.message)

    # def __str__(self):
    # return f"{self.message}"
