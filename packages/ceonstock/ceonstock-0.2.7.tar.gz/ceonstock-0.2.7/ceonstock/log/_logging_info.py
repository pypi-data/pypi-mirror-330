# Providers information and getters/printers for inspection of the current logging setup
import logging


def all_loggers() -> list[logging.Logger]:
    loggers = [logging.getLogger()]  # get the root logger
    loggers = loggers + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    return loggers


def print_all_loggers(print_fn: callable):
    loggers = all_loggers()
    printified_loggers_list = [_stringify_logger(logger) for logger in loggers]
    printified_loggers = _stringify_list(printified_loggers_list)
    print_fn(f"\n{printified_loggers}")


def _stringify_list(a: list, num_tabs: int=1) -> str:
    """ Concatanate a list of strings, placing each item on a newline. """
    if len(a) <= 0:
        return ''
    tabs = "\t" * num_tabs
    stringified = '\n'.join([f"{tabs}{list_item}" for list_item in a])
    return stringified

def _stringify_logger(logger: logging.Logger, num_tabs:int = 0):
    tabs = "\t" * num_tabs
    printable_string = f"{tabs}{logger}"

    handlers = logger.handlers
    if handlers:
        # Collect stringified handlers
        list_stringified_handlers = [f"{tabs}\t{handler}" for handler in handlers]
        stringified_handlers = _stringify_list(list_stringified_handlers, num_tabs=num_tabs+1)
        printable_string += f"\n{stringified_handlers}"
    # print(f"got handlers: {handlers}")

    return printable_string

