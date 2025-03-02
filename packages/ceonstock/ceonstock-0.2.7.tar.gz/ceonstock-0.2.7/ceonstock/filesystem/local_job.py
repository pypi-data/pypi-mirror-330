# A helper class that loads a target dir as a CstockProj
# Useful for validating the integrity of the job files
# Useful for identifying the file path that represents the job in a server with a filesystem
from __future__ import annotations
import logging
from typing import Union, Optional, List, Literal
from dataclasses import dataclass
from pathlib import Path

from ceonstock import json_io
from ceonstock import CstockJob

# from ceonstock.core.base import T
logger = logging.getLogger(__name__)


JOB_FOLDERS: dict[Literal["job_inputs", "job_outputs", "logs"], str] = {
    "job_inputs": "job_inputs",
    "job_outputs": "job_outputs",
    "logs": "logs",
}


class CstockLocalJobDirs:
    def __init__(self, job_root_dir: Union[Path, str]):
        self.root = Path(job_root_dir)
        self.job_inputs = Path(job_root_dir, "job_inputs")
        self.job_outputs = Path(job_root_dir, "job_outputs")
        self.logs = Path(job_root_dir, "logs")

    def create_directories(self):
        paths_to_make = []
        for path in self.__dict__.values():
            if not Path(path).exists():
                paths_to_make.append(path)
        stringified_paths = "\n\t".join([str(path) for path in paths_to_make])
        logger.info(f"Creating new folder(s):\n\t{stringified_paths}")
        for path in paths_to_make:
            Path(path).mkdir(parents=True, exist_ok=True)


class CstockLocalJob:
    json_file_name = "ceonstock_job.json"
    """
    Represents a job in the local filesystem.
    Provides functionality for loading data from files.
    """

    def __init__(
        self,
        job_dir_path: Union[Path, str],
        json_file_name: Optional[str] = None,
    ):
        self._dirs = CstockLocalJobDirs(job_dir_path)
        json_file_name = (
            json_file_name if json_file_name else CstockLocalJob.json_file_name
        )
        self._json_file_path = Path(self._dirs.root, json_file_name)
        if not self._dirs.root.is_dir():
            raise NotADirectoryError(
                f"LocalJob dir does not exist: {self._dirs.root}"
            )
        if not self._json_file_path.is_file():
            raise FileNotFoundError(
                f"LocalJob {self._dirs.root} missing expected JSON file: {self._json_file_path.name}"
            )

    def path(self) -> Path:
        return self._dirs.root

    def json_path(self) -> Path:
        return self._json_file_path

    def dirs(self) -> CstockLocalJobDirs:
        return CstockLocalJobDirs(self.path())

    def load(self) -> CstockJob:
        """
        Loads a CstockJob instance from the json file.
        Loading imports all data as python/ceonstock classes
        """
        logger.debug(f"Loading CstockJob({self.path()})...")
        cstock_job = json_io.job.from_file(
            str(self._json_file_path.absolute())
        )
        return cstock_job

    def __str__(self):
        return f"<{self.__class__.__name__} {self.path()}>"

    def __repr__(self):
        return self.__str__()


def create_local_job(
    job_dir: Union[str, Path], ceonstock_job: CstockJob
) -> CstockLocalJob:
    """Sets up the folders in the local filesystem and creates ceonstock_job.json"""
    if Path(job_dir).exists():
        raise Exception(
            f"Cannot create local job because the directory already exists: {job_dir}"
        )

    logger.info(f"{job_dir=}, {ceonstock_job=}")
    CstockLocalJobDirs(job_dir).create_directories()
    json_path = str(Path(job_dir, CstockLocalJob.json_file_name))
    json_io.job.to_file(json_path, ceonstock_job)

    ceonstock_local_job = CstockLocalJob(job_dir)
    return ceonstock_local_job
