#  https://realpython.com/python-json/
import json
import logging
from typing import Type, Callable, Dict, List
from functools import partial
from uuid import UUID

from ceonstock.core.base import CstockBaseClass
from ceonstock import (
    CstockProjInput,
    CstockProjectInfo,
    CstockRenderTask,
    CstockJobInput,
    CstockRenderPipeline,
)
from ceonstock.log import printify
from ceonstock import errors

logger = logging.getLogger(__name__)


def load_from_list(
    list_of_objects: List[dict], cstock_cls: Type[CstockBaseClass]
) -> List[CstockBaseClass]:
    return [cstock_cls(**object) for object in list_of_objects]


def load_from_dict(dict_from_json: dict, cstock_cls: Type[CstockBaseClass]):
    logger.info(f"Loading {cstock_cls.__name__} with dict: ")
    logger.info(f"{dict_from_json}")
    try:
        return cstock_cls(**dict_from_json)
    except TypeError as e:
        raise errors.CstockInstantiationError(
            cstock_cls=cstock_cls,
            errors=[str(e), f"Received:{printify(dict_from_json)}"],
        )


KEY_ACTION_MAP = {  # Special actions to be taken if a particular key is found
    "project_info": partial(load_from_dict, cstock_cls=CstockProjectInfo),
    "project_inputs": partial(load_from_list, cstock_cls=CstockProjInput),
    "job_inputs": partial(load_from_list, cstock_cls=CstockJobInput),
    "render_tasks": partial(load_from_list, cstock_cls=CstockRenderTask),
    "render_pipeline": partial(load_from_dict, cstock_cls=CstockRenderPipeline),
    "uuid": UUID,
    "task_uuid": UUID,
}


def decode_complex(dct):
    """
    Example of custom decoding logic.
    In this case a dict of
    {
        "__complex__": true,
        "real": 42,
        "imag": 36
    }
    Could be interpreted and loaded as a complex number object (python builtin) with:
    if "__complex__" in dct:
        return complex(dct["real"], dct["imag"])
    """
    # If a special key is detected, process the key's value with the appropriate function
    for key in dct.keys():
        if key in KEY_ACTION_MAP.keys():
            action_fn = KEY_ACTION_MAP[key]
            logger.debug(f"Found special key '{key}', running action: {action_fn}")
            dct[key] = action_fn(dct[key])
    return dct


LOAD_ARGS = {"object_hook": decode_complex}


def loads(json_string: str):
    return json.loads(json_string, **LOAD_ARGS)


def load(filepath):  # TODO
    return json.load(filepath, **LOAD_ARGS)
