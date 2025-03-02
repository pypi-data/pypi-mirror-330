import logging
from uuid import uuid4
from pathlib import Path
from typing import Optional, Union
from shutil import copy
from uuid import UUID

from ceonstock import CstockJob
from ceonstock.filesystem import local_job

logger = logging.getLogger(__name__)


def create_cstock_job_on_disk(
    cstock_job: CstockJob,
    jobs_dir: Union[str, Path],
    file_source_dirs: Union[list[Path], list[str]],
) -> UUID:
    """
    Create a job directory with ceonstock_job.json file and job_inputs files.
    jobs_dir: The root directory that contains all jobs.
    file_source_dirs: The dirs in where to look for input files.
    Returns: The uuid of the newly created job
    """
    logger.info(f"{cstock_job=} {jobs_dir=}, {file_source_dirs=}")
    job_uuid = cstock_job.job_uuid
    job_dir = Path(jobs_dir, str(job_uuid))
    # Creates the fodlers and json file
    cstock_local_job = local_job.create_local_job(
        job_dir=job_dir, ceonstock_job=cstock_job
    )

    # Copy the input files from value_picker source to job_inputs dir.
    for job_input in cstock_job.job_inputs:
        if not job_input.is_file_type:
            continue

        for value in job_input.values:
            source_file_path = _get_file_path(file_source_dirs, value)
            dest_path = Path(cstock_local_job.dirs().job_inputs, value)
            logger.info(
                f"Copying file:\n\tFrom: {source_file_path}\n\tTo: {dest_path}"
            )
            copy(source_file_path, dest_path)
    return UUID(job_uuid)


def _get_file_path(
    dirs_to_check: Union[list[str], list[Path]], file_name: str
) -> Path:
    """Receive a file_name and return the path to the source file"""
    dirs_to_check = [str(path) for path in dirs_to_check]
    files = []
    for dirpath in dirs_to_check:
        files += _list_files_in_dir(dirpath)
    for file in files:
        if Path(file).name == file_name:
            return file
    raise Exception(f"Could not find source file from name: {file_name}")


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
