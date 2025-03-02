import logging
from ceonstock.log import formats
from enum import Enum


class TerminalColor(Enum):
    GREY = "\x1b[38;20m"
    GREEN = "\x1b[32m"
    BLUE = "\x1b[34m"
    CYAN = "\x1b[36m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    RED_BOLD = "\x1b[31;1m"
    _RESET = "\x1b[0m"
