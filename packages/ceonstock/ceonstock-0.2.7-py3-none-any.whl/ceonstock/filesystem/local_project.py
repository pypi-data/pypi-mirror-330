# A helper class that loads a target dir as a CstockProj
# Useful for validating the integrity of the project files
# Useful for identifying the file path that represents the project in a server with a filesystem
import logging
from typing import Union
from pathlib import Path

from ceonstock import CstockProject
from ceonstock import json_io

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")


class CstockLocalProject:
    """
    Represents a folder in the local filesystem that contains a cstock project.
    Provides utility to load cstock clases from the local files.
    """

    def __init__(
        self,
        project_folder_path: Union[Path, str],
        json_file_name: str = "ceonstock_project.json",
    ):
        self._root = Path(project_folder_path)
        self._json_file_path = Path(self._root, json_file_name)
        if not self._root.is_dir():
            raise NotADirectoryError(
                f"Local_project dir does not exist: {self._root}"
            )
        if not self._json_file_path.is_file():
            raise FileNotFoundError(
                f"Local_project {self._root} missing expected JSON file: {self._json_file_path.name}"
            )

    def path(self) -> Path:
        return self._root

    def json_path(self) -> Path:
        return self._json_file_path

    def load(self) -> CstockProject:
        """
        Loads a CstockProject instance from the json file.
        Loading imports all data as python/ceonstock classes
        """
        logger.debug("\n\n")
        cstock_project = json_io.project.from_file(str(self.json_path()))
        logger.debug(
            f"Loaded CstockProject instance: {self.json_path()}\n{cstock_project}"
        )
        return cstock_project

    def __str__(self):
        return f"<{self.__class__.__name__} {self.path()}>"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.path()}>"
