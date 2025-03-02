# from .loggers import create_new_logger, module_logger
from .pretty_printer import printify

# Import formatters
from .formatters import ColoredFormatter
from .formatters_celery import CeleryTaskFormatter
from .formatters_celery import CeleryTaskFormatterColored
