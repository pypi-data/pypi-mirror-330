import logging
from typing import Union
from pathlib import Path
from json.decoder import JSONDecodeError

from . import exporter
from . import importer
from . import errors

logger = logging.getLogger(__name__)


def write_json_file(dict_data: dict, json_file_path: Union[Path, str]) -> str:
    json_data = exporter.dumps(dict_data)
    ensure_dir(Path(json_file_path).parent)
    with open(json_file_path, "w") as f:
        f.write(json_data)
    return json_data


def read_json_file(
    json_filepath: Union[str, Path], raise_empty_file=True
) -> str:
    # read json file
    if not Path(json_filepath).is_file():
        raise FileNotFoundError(
            f"Unable to find json file for json_file_path: {json_filepath}"
        )
    json_data = {}
    # Get data from file
    try:
        with open(str(json_filepath)) as f:
            json_data = importer.load(f)
    except JSONDecodeError as e:
        raise errors.InvalidJSONFileError(
            json_filepath, errors=["Failed to decode file", str(e)]
        )

    if not len(json_data) > 0:  # No data in file
        # print("No data found in file")
        if raise_empty_file:
            raise errors.InvalidJSONFileError(
                json_filepath,
                errors=["File does not contain data (empty JSON file)"],
            )
    # print(f"Got data in JSON({json_filepath}): {json_data}")

    return json_data


def ensure_dir(filepath: Union[Path, str]):
    """Create the dir if it doesn't already exist"""
    filepath = Path(filepath)
    if not filepath.exists():
        logger.info(f"Created new dir for json export: {filepath}")
        filepath.mkdir(parents=True)
