import json
from pathlib import Path

import core.job_input as cjob_input
import core.proj_input as cproj_input


def load_job_inputs(job_inputs: list[dict]) -> list[cjob_input.CstockJobInput]:
    loaded_job_inputs = list(map(cjob_input.CstockJobInput.from_dict, job_inputs))
    return loaded_job_inputs


def load_proj_inputs(proj_inputs: list[dict]) -> list[cproj_input.CstockProjInput]:
    loaded_proj_inputs = list(map(cproj_input.CstockProjInput.from_dict, proj_inputs))
    return loaded_proj_inputs



# Pair special keys with specific loaders
LOADERS = {
    "job_inputs": load_job_inputs,
    "proj_inputs": load_proj_inputs
}


def load(json_filepath: str, raise_empty_file=True):
    # read json file
    if not Path(json_filepath).is_file():
        raise FileNotFoundError(
            f"Unable to find json file for json_file_path: {json_filepath}"
        )
    json_data = {}
    # Get data from file
    try:
        with open(str(json_filepath)) as f:
            json_data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        raise Exception(f"Json failed to decode file for {json_filepath}: {e}")

    if not len(json_data) > 0:  # No data in file
        # print("No data found in file")
        if raise_empty_file:
            raise Exception(f"File does not contain data: {json_filepath}")
    # print(f"Got data in JSON({json_filepath}): {json_data}")

    loaded_data = dict_to_cstock(json_data)
    return loaded_data


def dict_to_cstock(json_dict_data: dict) -> dict:
    new_dict = {}
    for key in json_dict_data.keys():
        target_data = json_dict_data[key]
        if key in LOADERS.keys():
            loader_fn = LOADERS[key]
        else:
            loader_fn = None
        # print(f"key: {key}, loader: {loader_fn}")
        loaded_objects = loader_fn(target_data)
        # print(f"loaded objects: ")
        # for loaded_object in loaded_objects:
            # print(f"\t{loaded_object}")
        new_dict[key] = loaded_objects
    return new_dict


