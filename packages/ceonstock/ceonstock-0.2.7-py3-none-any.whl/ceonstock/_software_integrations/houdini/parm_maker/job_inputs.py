import importlib
from typing import Callable
from typing import List
from typing import Tuple

from . import hparms
from . import color
from .parm_types import HouParmType
from ceonstock import CstockJobInput, CstockJobInputType


# To prevent flake8 from failing on the string type-hints during CI
if False:
    import hou

importlib.reload(hparms)


def hou_parm_type(job_input_type: CstockJobInputType):
    return CSTOCK_TO_HOU[job_input_type]


def create_file_input_parm(parm_name: str, value: str):
    value_parm = hparms.create_file_parm(
        parm_name,
        label=parm_name,
        default_value=f"$CSTOCK_JOB/job_inputs/{value}",
    )
    return value_parm


def create_color_input_parm(parm_name: str, hex_value):
    value = list(color.color_hex_to_hou(hex_value))
    value_parm = hparms.create_color_parm(
        parm_name,
        label=parm_name,
        # default_value=[1, 0.2, 0.5],
        default_value=value,
    )
    return value_parm


def create_toggle_input_parm(parm_name: str, bool_value: bool):
    value = bool_value
    value_parm = hparms.create_toggle_parm(
        parm_name,
        label=parm_name,
        # default_value=[1, 0.2, 0.5],
        default_value=value,
    )
    return value_parm


def create_string_input_parm(parm_name, value):
    # TODO parse hex string to produce value
    value_parm = hparms.create_text_parm(
        parm_name, label=parm_name, default_value=value
    )
    return value_parm


# Map a function responsible for generating the parms for each cstock
# job input type. The function is expected to receive a name and
# a value, and returns a single hou.Parm.
CSTOCK_TO_HOU = {
    CstockJobInputType.IMG: create_file_input_parm,
    CstockJobInputType.STRING: create_string_input_parm,
    CstockJobInputType.COLOR: create_color_input_parm,
    CstockJobInputType.BOOL: create_toggle_input_parm,
}


def get_value_parm_fn(
    cstock_job_input_type: CstockJobInputType,
) -> Callable[[str, str], "hou.Parm"]:
    found_fn = CSTOCK_TO_HOU[cstock_job_input_type]
    return found_fn


def job_input_parms(cstock_job_input: CstockJobInput):
    """
    Receive a CstockJobInput instance.
    Returns a list of parms for the CstockJobInput instance.
    """
    print(f"Creating parms for job_input: {cstock_job_input}")
    new_parms = []  # List of hou parm instances
    job_input_name = cstock_job_input.name
    input_type = cstock_job_input.job_input_type
    # TODO setup 'entries' to store a value + metadata (e.g. img AR)
    entries = cstock_job_input.values or []

    num_entries_parm_name = f"{job_input_name}_num_entries"
    num_entries_parm = hparms.create_int_parm(
        num_entries_parm_name,
        label="Num Entries",
        default_value=len(entries),
    )
    new_parms.append(num_entries_parm)

    ###
    # Create a value parm for each entry in the job_input.
    ###
    # 'Value parm' is the parm that stores the received value for a particular
    # cstock_job_input entry.
    parm_fn = get_value_parm_fn(input_type)
    # TODO create 'entries' that store a value along with associated metadata.
    for i, value in enumerate(cstock_job_input.values or []):
        parm_name = f"{job_input_name}_{i}"
        value_parm = parm_fn(parm_name, value)
        new_parms.append(value_parm)

    return new_parms
