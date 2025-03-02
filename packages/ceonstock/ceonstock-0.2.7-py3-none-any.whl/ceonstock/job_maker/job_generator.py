import logging
import json
from typing import Union
from typing import Optional
from pathlib import Path
from enum import Enum

from ceonstock import CstockProject
from ceonstock import CstockProjectInput
from ceonstock import CstockJob
from ceonstock import CstockJobType
from ceonstock import CstockJobInput
from ceonstock import CstockJobInputType
from ceonstock.core.web_input import CstockWebInputType

from . import value_picker as vp

logger = logging.getLogger(__name__)


class FilePickerStrategy(Enum):
    ORDERED = "ordered"  # Get the first X found files
    RANDOM = "random"  # Randomly pick from all vailable files


# class FileSourceStrategy(Enum):
#     FOLDER_SETS = "folder_sets"  # List files inside a chosen folder
#     FILES = "files"  # List files that are not in a folder
#     ALL_FILES = "all_files"  # Create a list of all files, including subfolders


class DataPickerStrategy(Enum):
    FROM_FILE = "from_file"  # Read values from a json file on disk
    GENERATED = "generated"  # Random generation of values


class CstockJobGenerator:
    def __init__(
        self,
        # cstock_project: CstockProject,
        file_sources: Union[list[str], list[Path]],
        file_picker_strategy: Union[
            FilePickerStrategy, str
        ] = FilePickerStrategy.RANDOM,
        data_picker_strategy: Union[
            DataPickerStrategy, str
        ] = DataPickerStrategy.FROM_FILE,
        excluded_values: Optional[list] = None,
    ):
        """
        file_sources: A list of dirs containing files to be used as the job inputs.
        file_picker_strategy: The value_picker strategy used when choosing from files.
        data_picker_strategy: The value_picker strategy used when choosing from non-files.
        excluded_values: Values to be excluded from selection.
        """
        if not excluded_values:
            excluded_values = []
        # self.cstock_project = cstock_project
        if not isinstance(file_picker_strategy, FilePickerStrategy):
            file_picker_strategy = FilePickerStrategy(
                file_picker_strategy.lower()
            )
        if not isinstance(data_picker_strategy, DataPickerStrategy):
            data_picker_strategy = DataPickerStrategy(
                data_picker_strategy.lower()
            )

        self.file_sources = file_sources
        self.file_picker_strategy = file_picker_strategy
        self.data_picker_strategy = data_picker_strategy
        self.excluded_values = excluded_values

        # Maintain a list of value_pickers so that they can be used when/as intended
        self._value_pickers: dict[str, vp.CstockValuePicker] = {}

    def generate_job(
        self,
        cstock_project: CstockProject,
        job_type: CstockJobType = CstockJobType.PREVIEW,
    ) -> CstockJob:
        logger.warning(
            "TODO: Implement other file_picker_strategy (currently assumes to Random)"
        )
        job_inputs = []
        logger.debug(f"{self.file_sources=}")
        for project_input in cstock_project.project_inputs:
            logger.debug(f"Creating job_input for {project_input.name}")
            job_input = self.generate_job_input(project_input)
            logger.debug(f"Created job_input for {project_input.name}")
            job_inputs.append(job_input)

        logger.debug(f"Created {len(job_inputs)} job inputs:")
        job = CstockJob(
            job_inputs=job_inputs,
            project_uuid=str(cstock_project.project_uuid),
            job_type=job_type,
        )
        logger.debug(f"Created job:\n{job}")
        return job

    def generate_job_input(
        self, cstock_project_input: CstockProjectInput, num_entries=1
    ) -> CstockJobInput:
        logger.debug("Generating job input...")
        logger.warning(
            "TODO: Handle on_values_exhausted behaviour (error, cycle, repeat last value). (And make this a real generator with yeild?)"
        )
        value_picker = self._get_value_picker_for_project_input(
            cstock_project_input
        )
        chosen_values = value_picker.get_values(num_values=num_entries)
        logger.debug("Generated job input.")
        job_input = CstockJobInput(
            name=cstock_project_input.name,
            job_input_type=cstock_project_input.job_input_type,
            values=chosen_values,
        )
        return job_input

    def _get_value_picker_for_project_input(
        self, project_input: CstockProjectInput
    ) -> vp.CstockValuePicker:
        """Provides (and caches) a unique value picker for each project input"""
        value_picker = self._value_pickers.get(project_input.name)
        if value_picker:
            return value_picker

        logger.info(f"Creating new value picker for {project_input.name}")
        available_values = self._get_value_options_for_project_input(
            project_input
        )
        LOOKUP_STRATEGY = {
            FilePickerStrategy.ORDERED: vp.ValuePickerStrategy.ORDERED,
            FilePickerStrategy.RANDOM: vp.ValuePickerStrategy.RANDOM,
        }
        value_picker_strategy = LOOKUP_STRATEGY[self.file_picker_strategy]
        available_values_filtered = [
            value
            for value in available_values
            if value not in self.excluded_values
        ]
        new_value_picker = vp.CstockValuePicker(
            available_values_filtered,
            value_picker_strategy=value_picker_strategy,
        )
        logger.info(
            f"Created value picker for '{project_input.name}': {new_value_picker}"
        )
        self._value_pickers[project_input.name] = new_value_picker
        return new_value_picker

    def _get_value_options_for_project_input(
        self, project_input: CstockProjectInput
    ) -> list:
        """Handle the logic specific to this job_generator"""
        # Dropdowns provide their own values and will ignore the filesystem.
        logger.debug("Getting available values for job input generation...")
        if (
            project_input.web_input_type
            == CstockProjectInput.web_input_types.DROPDOWN
        ):
            available_options = _list_dropdown_values(project_input)
            return available_options

        if (
            project_input.job_input_type
            == CstockProjectInput.job_input_types.BOOL
        ):
            available_options = [False, True]
            return available_options

        # TODO implement different seleciton strategies.
        available_options = _get_value_options_from_files(
            self.file_sources, project_input
        )
        return available_options


def _list_dropdown_values(project_input: CstockProjectInput) -> list:
    """
    Extract the dropdown options from the project input and return the values as a list
    """
    if not project_input.web_input_type == CstockWebInputType.DROPDOWN:
        raise Exception(
            f"Cannot get dropdown options: Received project_input {project_input.name} is not a DROPDOWN web_input_type."
        )
    dropdown_options = project_input.type_settings["dropdown_options"]
    values = [option["value"] for option in dropdown_options]
    logger.debug(f"Got valid dropdown option values: {values}")
    return values


# def create_job_input(
#     project_input: CstockProjectInput, value_picker: vp.JobInputValuePicker
# ):
#     """
#     Create a job_input instance for the provided project_input
#     """
#     values = value_picker.get_values(project_input, num_values=5)
#     logger.debug(f"{value_picker} Got {len(values)} values:")
#     for value in values:
#         logger.debug(f"\t{value}")

#     return CstockJobInput(
#         name=project_input.name,
#         job_input_type=project_input.job_input_type,
#         values=values,
#     )


def _get_value_options_from_files(
    file_sources: Union[list[Path], list[str]],
    project_input: CstockProjectInput,
):
    """
    Return a list of available values for the current project_input.
    Values are sourced from self.file_sources, which are directories
    expected to follow an organizational structure.
        - File types are placed into folders.
        - Data types are stored in a json file with keys {arbitrary_name}: {value}
        (file_source_dir):
            doc/
                file1.docx.
                file2.docx.
            img/
                img1.jpg
                img2.png
            color.json <- {"white": "#AAAAAA", "black": "000000"}
    If multiple file_sources are provided, the available options will be combined.
    """
    if _is_file(project_input):
        # General case assumes the folder is named after the job_input_type
        fldr_name = project_input.job_input_type.lower()

        # Special cases, e.g. using only images generated from word docs
        # to match expected inputs for specific web_input_type
        if project_input.web_input_type == project_input.web_input_types.DOC:
            fldr_name = project_input.web_input_type.DOC.lower()

        files = []
        for file_source in file_sources:
            file_dir = Path(file_source, fldr_name)
            files += [file.name for file in _list_files_in_dir(file_dir)]
        logger.debug(f"Found {len(files)} from {len(file_sources)} sources.")
        return files

    # Read values from a json file
    possible_values = []
    json_filename = f"{project_input.job_input_type.lower()}.json"
    for file_source in file_sources:
        json_filepath = Path(file_source, json_filename)
        possible_values += _read_values_from_json_file(json_filepath)
    return possible_values


def _is_file(project_input) -> bool:
    file_types = [CstockJobInputType.IMG, CstockJobInputType.AUDIO]
    if project_input.job_input_type in file_types:
        return True
    return False


def _read_values_from_json_file(json_filepath: Union[Path, str]) -> list:
    """Read a json file on disk, return a list of values."""
    json_file = Path(json_filepath)
    if not json_file.is_file():
        raise FileNotFoundError(str(json_file))

    logger.debug(f"Reading json_file: {json_file}")
    with open(json_file) as f:
        json_str = f.read()
        data = json.loads(json_str)

    logger.debug("Loaded json data: ")
    for key, value in data.items():
        logger.debug(f"\t{key}: {value}")
    values = [value for value in data.values()]
    logger.debug(f"Got {len(values)} values from json file: ")
    for value in values:
        logger.debug(f"\t{value}")
    return values


def _list_files_in_dir(dir: Union[Path, str]) -> list[Path]:
    file_dir = Path(dir)
    if not file_dir.exists():
        raise NotADirectoryError(file_dir)
    filelist = file_dir.glob("**/*")
    files = [file for file in filelist if file.is_file()]
    logger.debug(f"Got {len(files)} files:")
    for file in files:
        logger.debug(f"\t{file}")
    return files
