import logging
import inspect
from typing import Optional, Type, List
from ceonstock.log import handlers

# For logging of the logging creation process
self_logger = logging.getLogger(__name__)
self_logger.setLevel("INFO")
self_logger.info(f"Self_logger {self_logger.name} initialized!")


def ceonstock_logger():
    """The parent logger for the ceonstock package"""
    return logging.getLogger("ceonstock")


def create_new_logger(
    logger_name: str,
    level: Optional[str] = None,
    handlers: Optional[List[logging.Handler]] = None,
):
    """
    Create a new logger.
    Raise an exception if the logger already exists.
    """
    if not handlers:
        handlers = []
    if logger_name in logging.Logger.manager.loggerDict.keys():
        raise Exception(f"Cannot create logger. Logger already exists: {logger_name}")
    # default_output_log = "logs/logs.log"
    self_logger.debug(f"Creating logger: {logger_name}")
    new_logger = logging.getLogger(logger_name)
    if level:
        new_logger.setLevel(level)
    for handler in handlers:
        new_logger.addHandler(handler)
    return new_logger


def module_logger(
    *, level: Optional[str] = None, handlers: Optional[List[logging.Handler]] = None
) -> logging.Logger:
    """
    Creates a logger with a name that matches the module name of the caller
    For example, when inside of
        ceonstock.core.job_input
    instead of creating a logger and using __name__, we can instead just use
    module_logger() and __name__ will be inherited automatically based
    on where module_logger() was called from.
    """
    self_logger.debug("TEST creating module logger")

    # Get the caller's module name. This saves having to pass __name__ as an arg
    # each time when setting up the logger
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])
    if not caller_module:
        return logging.getLogger("_unknown_module_logger_")
    caller_module_name = caller_module.__name__
    self_logger.debug(f"Caller: {caller_module_name}")

    module_logger = create_new_logger(
        caller_module_name, level=level, handlers=handlers
    )
    self_logger.info(f"Creating module logger: {module_logger.name}")
    return module_logger
