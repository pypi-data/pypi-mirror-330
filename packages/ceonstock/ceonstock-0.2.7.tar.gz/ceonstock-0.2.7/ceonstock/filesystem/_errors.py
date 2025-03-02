from pathlib import Path
from typing import Union, Optional, List
from ceonstock.errors import CstockError
from ceonstock.log import printify


class CstockLocalProjectError(CstockError):
    """Raised when trying to interact with a local project (files on disk)."""

    def __init__(
        self,
        project_path: Union[Path, str],
        message=None,
        errors: Optional[List] = None,
    ):
        if not message:
            message = f"Failed to load local project {project_path}"
        self.message = message
        self.errors = errors
        if errors:
            self.message += ":" + printify(errors)
        super().__init__(self.message)


class CstockLocalJobError(CstockError):
    """Raised when trying to interact with a local job (files on disk)."""

    def __init__(
        self,
        job_path: Union[Path, str],
        message=None,
        errors: Optional[List] = None,
    ):
        if not message:
            message = f"Failed to load local job {job_path}"
        self.message = message
        self.errors = errors
        if errors:
            self.message += ":" + printify(errors)
        super().__init__(self.message)
