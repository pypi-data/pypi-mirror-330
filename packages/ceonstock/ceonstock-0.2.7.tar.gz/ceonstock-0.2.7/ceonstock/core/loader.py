import logging
import inspect
from typing import Type, TypeVar
from ceonstock import errors

T = TypeVar("T")

logger = logging.getLogger(__name__)


def cstock_from_dict(dict_kwargs: dict, cls_to_instantiate: Type[T]) -> T:
    """
    Init from a dict, but fail and reporting if unrecognized kwargs are found.
    -
    This was added because instantiating with cls(**kwargs_dict) silently ignores unrecognized kwargs
    when running in FastAPI (FastAPI overrides dataclasses default behaviour with pydantic versions???).
    This meant that projects which were identified as valid in the webUI/FileServer would fail when trying to run
    on the render server (if unrecognized kwargs were found).
    Therefore, use this function to instantiate classes from a dict.
    """
    unrecognized_kwargs = []
    known_kwargs = {}
    for k, v in dict_kwargs.items():
        if k in inspect.signature(cls_to_instantiate).parameters:
            known_kwargs[k] = v
        else:
            unrecognized_kwargs.append(k)

    if unrecognized_kwargs:
        logger.warning(
            f"Received {len(unrecognized_kwargs)} unrecognized kwargs: {unrecognized_kwargs}"
        )
        raise errors.CstockInstantiationError(
            cstock_cls=cls_to_instantiate,
            message=f"Unrecognized kwargs: {unrecognized_kwargs}",
        )

    return cls_to_instantiate(**known_kwargs)
