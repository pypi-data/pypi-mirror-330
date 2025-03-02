from typing import Union, Type, Optional, List
from pathlib import Path

# from ceonstock.errors import CstockError


class EmptyJSONFileError(Exception):
    """Raised when a JSON file is found, but does not contain any content"""


class InvalidJSONFileError(Exception):
    """Raised when a JSON file is found, but could not be decoded"""

    def __init__(
        self, file_path: Union[str, Path], errors: Optional[list] = None
    ):
        self.file_path = str(file_path)
        self.errors = errors
        self.message = f"Failed to read json file {file_path}"
        if errors:
            self.message += ": " + str(errors)
        super().__init__(self.message)


# class CstockImportError(CstockError):
#     """Raised when trying to load an object from json data"""

#     def __init__(
#         self,
#         file_path: Union[str, Path],
#         class_to_instantiate: Type,
#         errors: Optional[List] = None,
#     ):
#         self.file_path = str(file_path)
#         self.class_to_instantiate = class_to_instantiate.__name__
#         self.errors = errors
#         self.message = (
#             f"Failed to import class {class_to_instantiate.__name__} from {file_path}"
#         )
#         if errors:
#             self.message += ": " + str(errors)
#         super().__init__(self.message)
