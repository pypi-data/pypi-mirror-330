# Import/Export for a ceonstock job
# To avoid polluting the base classes implement (de)serialization tools in this module directly,
import json
from dataclasses import asdict
from ceonstock.core import CstockJob
from ceonstock.core.job_input import CstockJobInput, CstockJobInputType

# POSSIBLE ALTERNATIVE dataclass-wizard.
#    https://dataclass-wizard.readthedocs.io/en/latest/
# dataclass_wizard:
# - Expects enums to use VALUES by default: 'color' not 'COLOR'
# - Only provider one error at a time on failure.
# - Doesn't require schema class, just use fromdict and asdict methods directly.
# - Good documentation and seems to be easy to config

# from dataclass_wizard import fromdict, asdict, DumpMeta


# marshmallow:
# - Gives cleaerer errors (reports all together)
# - Expects enums to use NAME not VALUE, e.g. 'COLOR' not 'color'
# - Requires instantiating the schema class first

# Chose to use marshmallow for the multi-error reporting. NOTE: enum NAME vs VALUE could cause
# some compatibility problems with workflows that expect values? It's possible to configures
# marshmallow but haven't looked into it yet and seems to not support enums contained
# within a list?

# Keep dataclass_wizard available as a backup in case the enum naming convention causes problems in the
# future? (Or learn how to configure marshmallow to use enum values)

# import marshmallow_dataclass

# Create a marshmallow schema instance to use for (de)serialization operations.
# job_schema = marshmallow_dataclass.class_schema(CstockJob)()


def _job_input_from_dict(dict_data) -> CstockJobInput:
    prepared_dict = dict_data.copy()
    try:
        # Load from enum VALUE
        job_input_type = CstockJobInputType(dict_data["job_input_type"])
    except ValueError:
        # Load from enum NAME
        job_input_type = CstockJobInputType[dict_data["job_input_type"]]
    prepared_dict["job_input_type"] = job_input_type
    return CstockJobInput(**prepared_dict)


def from_dict(dict_data) -> CstockJob:
    """
    Load a CstockJob instance from a received json dict.
    """
    prepared_dict = dict_data.copy()
    prepared_dict["job_inputs"] = [
        _job_input_from_dict(data) for data in dict_data["job_inputs"]
    ]
    return CstockJob(**prepared_dict)


def from_file(file_path: str) -> CstockJob:
    with open(file_path, "r") as f:
        data = json.load(f)
    job = from_dict(data)
    return job


def to_file(file_path: str, job: CstockJob) -> str:
    """Save a CstockJob to a json file.
    Returns: The path of the newly saved file as a string"""

    job_dict = to_dict(job)

    with open(file_path, "w") as f:
        json.dump(job_dict, f, indent=2)
    return file_path


def to_dict(job: CstockJob) -> dict:
    """Save a CstockJob to a json file.
    Returns: The path of the newly saved file as a string"""

    job_dict = asdict(job)

    return job_dict
