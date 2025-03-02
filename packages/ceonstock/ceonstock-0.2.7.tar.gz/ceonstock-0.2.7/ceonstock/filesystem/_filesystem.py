import os, glob, shutil, json
import logging
from dataclasses import dataclass
from typing import Optional, Union, List
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def copy_file(source_file: Path, dest_file: Path) -> Path:
    logger.debug(f"Copying file {source_file} to {dest_file}")
    out_dir = dest_file.parent
    if not dest_file.parent.exists():
        logger.warn(f"Created directory: {out_dir}")
        out_dir.mkdir(parents=True)
    new_file = shutil.copy(str(source_file), str(dest_file))
    return Path(new_file)


def create_directories(*paths_to_create):
    for path in paths_to_create:
        if not Path(path).exists():
            logger.info(f"Creating new folder(s): {path}")
            Path(path).mkdir(parents=True, exist_ok=True)
    """
    for path in list_of_paths
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"Created new folder(s): {path}")
    """


def get_files_from_folder(
    root_folder, recursive=True, raise_missing_folder=True
) -> List[Path]:
    # files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not Path(root_folder).is_dir():
        # TODO also confirm that the folder contains files?
        logger.warn(f"Folder does not exist: {root_folder}")
        if raise_missing_folder:
            raise Exception(f"Missing required root_folder dir: {root_folder}")
        return []
    files = glob.glob(root_folder + "/**/*", recursive=recursive)
    logger.info(f"Found files in {root_folder}: {files}")
    return files


async def save_file_to_disk(file_obj, output_file_path):
    # file_name = user_file.filename
    logger.info(f"Received an image: {file_obj}")
    with open(output_file_path, "wb+") as f:
        shutil.copyfileobj(file_obj.file, f)
    logger.info(f"Image saved to: {output_file_path}")
    return output_file_path


def zip_dir(dir_to_zip, output_zip_file_path, overwrite=False, raise_skipped_zip=False):
    # Zip project
    logger.info(f"Zipping dir {dir_to_zip} as: {output_zip_file_path}")
    output_zip_file = Path(output_zip_file_path)
    zip_dir = output_zip_file.parent
    if not zip_dir.exists():
        logger.warn(f"Dir does not exist: {zip_dir}")
        return None
    if not output_zip_file.suffix:
        logger.warn("Invalid output_zip_file_path (not a valid file path with ext)")
        return None
    if output_zip_file.exists() and not overwrite:
        msg = f"Skipping zip (already exists!): {output_zip_file_path} "
        if raise_skipped_zip:
            raise Exception(msg)
        logger.warn(msg)
        return None
    zip_type = str(output_zip_file.suffix).lstrip(".")
    logger.debug(f"Got zip type: {zip_type}")
    file_basename = output_zip_file.stem
    logger.debug(f"Got basename: {file_basename}")
    output_file_no_ext = f"{zip_dir}/{file_basename}"
    if output_zip_file.exists():
        logger.warn(f"File already exists! Overwriting: {output_zip_file_path}")
    new_zip = shutil.make_archive(output_file_no_ext, zip_type, dir_to_zip)
    logger.info(f"Successfully created zip: {new_zip}")
    return Path(new_zip)


def unzip_file(zip_file, create_folder=False, output_dir=None):
    if not os.path.isfile(zip_file):
        logger.warn(f"Project zip file not found!: {zip_file}")
        logger.debug(f"Skipping... {zip_file} (Not Found!)")
        return None
    if not output_dir:
        output_dir = Path(zip_file).parent

    if not os.path.isdir(output_dir):
        raise Exception(f"output_dir does not exist: {output_dir}")

    if create_folder:
        fldr_name = Path(zip_file).stem
        extract_to_dir = f"{output_dir}/{fldr_name}"
        if not os.path.isdir(extract_to_dir):
            os.mkdir(extract_to_dir)
    else:
        extract_to_dir = f"{output_dir}"

    logger.info(f"Unzipping: {zip_file} to {extract_to_dir}")
    shutil.unpack_archive(zip_file, extract_dir=extract_to_dir)
    logger.debug("Unzip complete")
    return extract_to_dir


def read_json_file(file_path):
    with open(file_path) as f:
        json_data = json.load(f)
    return json_data


@dataclass
class FileCheckReport:
    expected: List[str]
    found: List[str]
    missing: List[str]

    def __post_init__(self):
        if len(self.found) + len(self.missing) != len(self.expected):
            raise Exception(
                f"Failed to validate FileCheckReport. found({len(self.found)}) + missing({len(self.missing)}) != num expected({len(self.expected)})"
            )


def check_for_anomaly_files(local_dir, expected_files):
    """Returns any files in the target dir that are NOT expected"""
    local_file_list = get_files_from_folder(local_dir)
    return [file for file in local_file_list if file not in expected_files]


def check_for_expected_files(
    expected_files: Union[List[Path], List[str]]
) -> FileCheckReport:
    """Returns an object containing lists of found and missing files"""
    logger.debug(f"Got expected_files: {expected_files}")
    filepath_strings = [str(file) for file in expected_files]
    files_found = []
    files_missing = []
    for file in filepath_strings:
        if Path(file).is_file():
            files_found.append(file)
        else:
            files_missing.append(file)
    return FileCheckReport(
        expected=filepath_strings,
        found=files_found,
        missing=files_missing,
    )
