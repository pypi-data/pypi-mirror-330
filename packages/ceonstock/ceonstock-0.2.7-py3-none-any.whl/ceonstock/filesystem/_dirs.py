from dataclasses import dataclass
from typing import Dict, List, Union
from pathlib import Path


@dataclass
class SubmissionDirFolderNames:
    entries = ""
    preprocess = "preprocess"
    meta = "meta"
    logs = "logs"


@dataclass
class SubmissionDirs:
    root: Union[Path, str]
    fldr_names: SubmissionDirFolderNames = SubmissionDirFolderNames()

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self.entries = self.root / self.fldr_names.entries
        self.preprocess = self.root / self.fldr_names.preprocess
        self.meta = self.root / self.fldr_names.meta
        self.logs = self.root / self.fldr_names.logs

    def __str__(self):  # str method determines how this class is shown when printed
        return f"<{self.__class__.__name__}: {self.root}>"

    def dirs(self) -> Dict[str, Path]:
        return {
            "root": self.root,
            "entries": self.entries,
            "preprocess": self.preprocess,
            "meta": self.meta,
            "logs": self.logs,
        }


@dataclass
class JobDirFolderNames:
    job_inputs = "job_inputs"
    job_outputs = "job_outputs"
    meta = "meta"
    logs = "logs"


@dataclass
class JobDirs:
    root: Union[Path, str]
    fldr_names: JobDirFolderNames = JobDirFolderNames()

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self.job_inputs = self.root / self.fldr_names.job_inputs
        self.job_outputs = self.root / self.fldr_names.job_outputs
        self.meta = self.root / self.fldr_names.meta
        self.logs = self.root / self.fldr_names.logs

    def __str__(self):  # str method determines how this class is shown when printed
        return f"<JobDirs: {self.root}>"

    # TODO deprecate this in favor of to_dict()
    def dirs(self) -> Dict[str, Path]:
        return self.to_dict()

    def to_dict(self) -> Dict[str, Path]:
        return {
            "root": Path(self.root),
            "job_inputs": self.job_inputs,
            "job_outputs": self.job_outputs,
            "logs": self.logs,
            "meta": self.meta,
        }


def create_dirs(dirs_to_create: List[Path]) -> List[Path]:
    new_dirs = []
    for path in dirs_to_create:
        if not path.exists():
            Path(path).mkdir(parents=True)
            new_dirs.append(path)
    return new_dirs
