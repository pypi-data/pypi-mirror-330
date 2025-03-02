import json
import logging
from uuid import UUID
from typing import Any

from ceonstock.core.base import CstockBaseClass

logger = logging.getLogger(__name__)


# Allow handling of non-serializable types
class CstockJsonEncoder(json.JSONEncoder):
    def default(self, value: Any):
        """JSON serialization conversion function."""

        # Handle serialization of otherwise unserializable types
        if isinstance(value, UUID):
            return str(value)

        if isinstance(value, CstockBaseClass):
            return value.__dict__
            # return json.loads(json.dumps(value.__dict__, **DUMP_ARGS))

        # Here you can have other handling for your
        # IPV4, or datetimes, or whatever else you
        # have.

        # Otherwise, default to super
        return super(CstockJsonEncoder, self).default(value)


DUMP_ARGS = {"cls": CstockJsonEncoder, "indent": 4, "sort_keys": True}


# TODO allow kwargs in case user want to overwrite defaults
def dumps(some_dict: dict):
    return json.dumps(some_dict, **DUMP_ARGS)


# TODO allow kwargs in case user want to overwrite defaults
def dump(some_dict, fp):
    return json.dump(some_dict, fp, **DUMP_ARGS)
