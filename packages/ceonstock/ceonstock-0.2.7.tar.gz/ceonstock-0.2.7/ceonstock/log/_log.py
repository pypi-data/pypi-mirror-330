import logging
from pathlib import Path


def init_self_logger():
    self_logger = logging.getLogger(__name__)
    # self_logger.setLevel("INFO")
    self_logger.setLevel("DEBUG")
    self_logger.info("This is self_logger before parent handler check")

    self_logger.info("Self_logger initialized!")
    return self_logger


def setup_root_logger(preserve_existing_handlers=True, level=None):
    self_logger.info("Setting up root logger...")
    root_logger = logging.getLogger()
    formatter = get_formatter("DEV")
    if root_logger.handlers:
        if preserve_existing_handlers:  # Root already has handler(s)
            for handler in root_logger.handlers:
                self_logger.info("\t...overwriting formatter only")
                handler.setFormatter(formatter)
            return
        else:
            self_logger.info("Deleting existing root handlers...")
            root_logger.handlers.clear()
    self_logger.info("root logger has no handlers!")
    self_logger.info("Adding new handler...")
    # Setup stream handler
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    if level:
        sh.setLevel(level)
    root_logger.addHandler(sh)
    self_logger.info("Added new handler to root logger.")


class ColoredFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[32m"
    blue = "\x1b[34m"
    cyan = "\x1b[36m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    msg_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    def __init__(self, string_for_format: str):
        self.msg_format = ColoredFormatter.msg_format
        if string_for_format:
            self.msg_format = string_for_format

    def get_format(self, levelno):
        COLORS = {
            logging.DEBUG: ColoredFormatter.blue,
            logging.INFO: ColoredFormatter.grey,
            logging.WARNING: ColoredFormatter.yellow,
            logging.ERROR: ColoredFormatter.red,
            logging.CRITICAL: ColoredFormatter.bold_red,
        }
        chosen_color = COLORS.get(levelno, "")
        return chosen_color + self.msg_format + ColoredFormatter.reset

    def format(self, record):
        log_fmt = self.get_format(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_formatter(formatter_name: str) -> logging.Formatter:
    dev_formatter = ColoredFormatter(
        "%(levelname)s: [%(name)s:%(lineno)d] %(funcName)s(): %(message)s"
    )
    prod_formatter = logging.Formatter(
        "[%(name)s] %(levelname)s: %(funcName)s(): %(message)s (%(filename)s:%(lineno)d)"
    )
    formatters = {"DEV": dev_formatter, "PROD": prod_formatter}
    formatter = formatters.get(formatter_name, prod_formatter)
    return formatter


def add_stream_handler(logger):
    formatter = get_formatter("DEV")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    self_logger.info(f"Added streamHandler to: {logger.name}")


# TODO how to use logger to print messages for log creation?
# ^(without manually creating one without this function)
def print_all_loggers():
    # loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    logger_names = [name for name in logging.root.manager.loggerDict]
    """
    loggers = [
        {logging.getLogger(name): logging.getLogger(name).handlers}
        for name in logging.root.manager.loggerDict
    ]
    """
    self_logger.info(f"LOGGERS: {logger_names}")


def list_all_logger_handlers(include_null_handler=False):
    loggers = [logging.getLogger()]  # get the root logger
    loggers = loggers + [
        logging.getLogger(name) for name in logging.root.manager.loggerDict
    ]
    list_of_handlers = []
    for logger in loggers:
        for handler in logger.handlers:
            if include_null_handler or handler.__class__.__name__ != "NullHandler":
                list_of_handlers.append(f"Logger {logger} has handler {handler}")
    return list_of_handlers


def print_logger_handlers(logger_to_check):
    if logger_to_check.handlers:  # Root already has handler(s)
        self_logger.info("Found handlers!")
        for handler in logger_to_check.handlers:
            self_logger.info(f"\t{handler}")
    else:
        self_logger.info(f"Logger({logger_to_check.name}) does not have any handlers!")


# To prevent duplicate logging due to uvicorn propogation
# From https://github.com/encode/uvicorn/issues/630
def disable_uvicorn_root_logger():
    """Uvicorn adds a default handler to the root logger,
    so all logs messages are duplicated"""
    uvicorn_logger = logging.getLogger("uvicorn")
    if logging.root.handlers:
        self_logger.info(f"Got root handlers: {logging.root.handlers}")
        # Move the root logger over to the "uvicorn" logger and clear the root
        uvicorn_logger.addHandler(logging.root.handlers[0])
        logging.root.handlers = []
        uvicorn_logger.propagate = False
        self_logger.info("Disabled uvicorn root logger!")
    self_logger.info(
        "disable_uvicorn_root_logger() Did not find any root logging handlers"
    )


self_logger = init_self_logger()
if not self_logger.hasHandlers():
    setup_root_logger()
else:
    self_logger.info("This logger (or a parent) has a handler")
