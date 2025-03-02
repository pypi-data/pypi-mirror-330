import json
import logging
from typing import Union
from pathlib import Path
from uuid import UUID
from dataclasses import asdict

from ceonstock.core.base import CstockBaseClass
from ceonstock.core.base import CstockBaseEnum

logger = logging.getLogger(__name__)


class CstockJsonEncoder(json.JSONEncoder):
    """Allow JSON saving of non-serializable types"""

    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)

        if isinstance(obj, CstockBaseClass):
            return asdict(obj)

        return json.JSONEncoder.default(self, obj)


DUMP_ARGS = {"cls": CstockJsonEncoder, "indent": 4, "sort_keys": True}


def dumps(some_dict: dict):
    return json.dumps(some_dict, **DUMP_ARGS)


def dump(some_dict: dict, fp):
    return json.dump(some_dict, fp, **DUMP_ARGS)


def save_json(json_filepath: Union[str, Path], json_data: dict):
    """
    Save json file.
    Uses a custom Encoder to handle unserializable types.
    """
    logger.debug(f"Saving json data: {json_data}")
    file_dir = Path(json_filepath).parent
    if not file_dir.is_dir():
        logger.info(f"Creating dir: {file_dir}")
        file_dir.mkdir(exist_ok=True, parents=True)
    with open(json_filepath, "w") as f:
        f.write(dumps(json_data))
    logger.info(f"Saved json file: {json_filepath}")


def save_ceonstock_json(
    json_filepath: Union[str, Path], ceonstock_instance: CstockBaseClass
):
    """
    Save a ceonstock_instance to a json file.
    Uses a custom Encoder to handle unserializable types.
    """
    logger.info(f"Saving json from ceonstock instance: {ceonstock_instance}")
    dict_data = asdict(ceonstock_instance)
    logger.debug(f"Created dict data: {dict_data}")
    with open(json_filepath, "w") as f:
        f.write(dumps(dict_data))
    logger.info(f"Saved json file: {json_filepath}")
