import logging
import json
from dataclasses import asdict
from typing import List, Dict, Any, Callable
from typing import Optional, Union, Type
from typing import Iterable

logger = logging.getLogger(__name__)

BRACES_LIST = ("[", "]")
BRACES_DICT = ("{", "}")


def printify(data: Any, indent: int = 1) -> str:
    logger.debug(f"Got data of type {type(data)}: {data}")
    """ Returns data object as a string formmatted for printing """
    fn = get_printify_function(data)
    logger.debug(f"Chosen fn: {fn}")
    as_str = fn(data, indent=indent)
    return as_str


def get_printify_function(data: Iterable) -> Callable:
    LOOKUP = {dict: printify_dict, list: printify_list}
    logger.debug(f"LOOKUP: {LOOKUP}")
    try:
        fn = LOOKUP[type(data)]
    except KeyError as e:
        logger.debug(f"KeyError: {e}")
        try:
            # Check if the object is a class instance containing a __dict__ method.
            test = data.__dict__
            return printify_class
        except AttributeError:
            logger.warn(f"Invalid data type: {type(data)}")
        return printify_str
    logger.debug(f"fn: {fn}")
    return fn


def printify_str(data, indent=1) -> str:
    tabs = "\t" * indent
    return tabs + str(data)


# def printify_dict(data: Dict, indent: int = 1) -> str:
#     """Returns data object as a string formmatted for printing"""
#     dict_to_print = {key: str(value) for (key, value) in data.items()}
#     tabs = "\t" * indent
#     lines = []
#     for key, value in dict_to_print.items():
#         lines.append(f"{tabs}{key}:\t{value}")
#     _add_surrounding_braces(lines, BRACES_DICT, indent=indent - 1)
#     as_str = "\n".join([line for line in lines])
#     return as_str


def printify_dict(data: Dict, indent: int = 1) -> str:
    """Returns data object as a string formmatted for printing"""
    dict_to_print = {key: str(value) for (key, value) in data.items()}
    return json.dumps(dict_to_print, indent=4)


def printify_list(data: list, indent: int = 1) -> str:
    """Returns list object as a string formmatted for printing"""
    list_to_print = [str(value) for value in data]
    tabs = "\t" * indent

    lines = []
    for item in list_to_print:
        lines.append(f"{tabs}{item}")
    _add_surrounding_braces(lines, indent=indent - 1, brace_chars=BRACES_LIST)
    as_str = "\n".join([line for line in lines])
    return as_str


def printify_class(data, indent: int = 1) -> str:
    # Printify a class by converting it to a dict.
    try:
        return printify_dict(asdict(data))
    except Exception as e:
        logger.warning(f"TODO: handle not-a-dataclass error: {e}")
    return printify_dict(data.__dict__, indent=indent)


def _add_surrounding_braces(
    lines: list[str], brace_chars: tuple[str, str], indent=0
):
    """Add braces to the start and end of the list containing the lines to be printed."""
    indent = max(0, indent)
    brace_tabs = "\t" * indent
    lines.insert(0, f"{brace_tabs}{brace_chars[0]}")
    lines.append(f"{brace_tabs}{brace_chars[1]}")
