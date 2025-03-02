import logging
import inspect
from typing import Type, TypeVar
from typing import Union
from uuid import UUID
from ceonstock import errors
from ceonstock.core.base import CstockBaseEnum
from ceonstock.core.loader import cstock_from_dict

logger = logging.getLogger(__name__)

import logging
import inspect
from typing import Type, TypeVar
from ceonstock import errors

T = TypeVar("T")

logger = logging.getLogger(__name__)


E = TypeVar("E", bound="CstockBaseEnum")
T = TypeVar("T")


def enforce_enum(received: CstockBaseEnum, expected_cls: Type[E]) -> E:
    """Cast to the expected enum and return"""
    if isinstance(received, expected_cls):
        return received
    if isinstance(received, CstockBaseEnum):  #  Wrong enum type was provided
        # Prevent other Cstock enum types with matching string values from being
        # silently converted
        raise errors.CstockUnknownTypeError(
            received=received, expected=expected_cls
        )
    return expected_cls(received)


def enforce_uuid(received: UUID) -> UUID:
    """Cast to the expected enum and return"""
    if isinstance(received, UUID):
        return received
    return UUID(received)


def enforce_class_instance(item: Union[dict, Type], cls_to_enforce: Type):
    if isinstance(item, cls_to_enforce):
        return item
    try:
        if isinstance(item, dict):
            # Use the cstock loader from_dict to force errors to be thrown
            # even when instantiating dataclasses on a fastapi server (fastapi overrides
            # the default behaviour when cls(**kwargs), causing invalid kwargs to be ignored
            # even though the same code throws an error in non-fast-api contexts.)
            item = cstock_from_dict(item, cls_to_enforce)
            return item
        if isinstance(item, list):
            item = cls_to_enforce(*item)
            return item
        item = cls_to_enforce(item)
        return item
    except Exception as e:
        raise errors.CstockInstantiationError(
            cstock_cls=cls_to_enforce,
            errors=[
                f"Could not instantiate class instance, received item of type {type(item)} could not be instantiated as an instance of {cls_to_enforce.__name__}: {item=} {e=}"
            ],
        )


def enforce_list_of_instances(list_of_objects, cls_to_enforce: Type):
    if not isinstance(list_of_objects, list):
        raise Exception(
            "Enforce list of instances expects to receive a list (TODO: Auto-wrap non-list as a list?)"
        )
    enforced_list = [
        enforce_class_instance(list_item, cls_to_enforce)
        for list_item in list_of_objects
    ]
    return enforced_list
