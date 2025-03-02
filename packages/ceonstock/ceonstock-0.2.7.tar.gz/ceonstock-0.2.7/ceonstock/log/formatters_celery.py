# A custom Formatter that injects extra variables that can be used in the format string.
# In this case we add task_name and task_id.
import logging
import time

from enum import Enum

from .colors import TerminalColor


# Modify the default formatter to inject extra parameters
# which can be used in the format string
class CeleryTaskFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from celery._state import get_current_task

            self.get_current_task = get_current_task
        except ImportError:
            self.get_current_task = lambda: None

    def formatTime(self, record, datefmt=None):
        """Processes the %(asctime)s arg in the format string.
        Modified to include the use of %f and %z for milliseconds/timezone
        in the datefmt string"""
        ct = self.converter(record.created)
        if datefmt:
            # support %z and %f in datefmt (struct_time doesn't carry ms or tz)
            datefmt = datefmt.replace("%f", "%03d" % int(record.msecs))
            datefmt = datefmt.replace("%z", time.strftime("%z"))
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = "%s,%03d" % (t, record.msecs)
        return s

    def format(self, record):
        # Modify the recored.__dict__ to add extra properties that can
        # be used for formatting.
        task = self.get_current_task()
        if task and task.request:
            task_kwargs = task.request.kwargs
            job_uuid = task_kwargs.get("job_uuid")
            task_name = task.name
            # Trim the taskname by lstripping redundant parts: app.task.
            task_name = _lstrip_substring(task_name, "app.")
            task_name = _lstrip_substring(task_name, "tasks.")
            task_name = task_name.lstrip(".")
            record.__dict__.update(
                task_id=task.request.id, task_name=task_name, job_uuid=job_uuid
            )
        else:
            record.__dict__.setdefault("task_name", "")
            record.__dict__.setdefault("task_id", "")
            record.__dict__.setdefault("job_uuid", "")
        return super().format(record)


def _lstrip_substring(string_to_check: str, substring_to_remove: str):
    if not string_to_check.startswith(substring_to_remove):
        return string_to_check
    return string_to_check[len(substring_to_remove) :]


# Wrap the task formatter with colouring functionality.
class CeleryTaskFormatterColored(CeleryTaskFormatter):
    default_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def __init__(self, string_for_format: str, *args, **kwargs):
    #     self.msg_format = TaskFormatterColored.default_format
    #     if string_for_format:
    #         self.msg_format = string_for_format
    #     # super().__init__(self.msg_format, *args, **kwargs)

    def get_color(self, levelno):
        COLORS = {
            logging.DEBUG: TerminalColor.BLUE,
            logging.INFO: TerminalColor.GREY,
            logging.WARNING: TerminalColor.YELLOW,
            logging.ERROR: TerminalColor.RED,
            logging.CRITICAL: TerminalColor.RED_BOLD,
        }
        chosen_color = COLORS.get(levelno, "")
        return chosen_color

    def apply_color(self, formatted_msg: str, terminal_color: TerminalColor):
        # The color formatting must be applied to each line individually to take effect
        # over newlines.
        colored_lines = []
        for line in formatted_msg.split("\n"):
            colored_line = f"{terminal_color.value}{line}{TerminalColor._RESET.value}"
            colored_lines.append(colored_line)
        colored_msg = "\n".join(colored_lines)
        return colored_msg

    def format(self, record):
        formatted_msg = super().format(record)
        chosen_color = self.get_color(record.levelno)
        colored_msg = self.apply_color(formatted_msg, chosen_color)
        return colored_msg


# class TaskFormatterColored(formatters.ColoredFormatter, TaskFormatter):
#     pass


""" Example Usage:
logger = logging.getLogger()
sh = logging.StreamHandler()
sh.setFormatter(
    TaskFormatter(
        '%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'))
logger.setLevel(logging.INFO)
logger.addHandler(sh)
"""
