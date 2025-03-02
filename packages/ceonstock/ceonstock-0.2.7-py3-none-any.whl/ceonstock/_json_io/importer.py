import json
import inspect
import logging
from pathlib import Path
from typing import Union
from typing import TypeVar
from typing import Type
from ceonstock import errors

logger = logging.getLogger()

T = TypeVar("T")


def loads(json_string: str):
    return json.loads(json_string)


def load(json_filepath: Union[Path, str]):
    if not Path(json_filepath).is_file():
        raise FileNotFoundError(
            f"Unable to find json file for json_file_path: {json_filepath}"
        )
    with open(str(json_filepath)) as f:
        json_data = json.load(f)
    return json_data


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
    try:
        return cls_to_instantiate(**known_kwargs)
    except TypeError as e:
        # Catch TypeError if cls_to_instantiate is missing required args. Re-raise as InstantiationError
        raise errors.CstockInstantiationError(cstock_cls=cls_to_instantiate, errors=e,message="Failed to instantiate class instance from dict.")


def cstock_from_json(
    json_filepath: Union[Path, str], cstock_cls: Type[T]
) -> T:
    json_data = load(json_filepath)
    cstock_instance = cstock_from_dict(json_data, cstock_cls)
    return cstock_instance
