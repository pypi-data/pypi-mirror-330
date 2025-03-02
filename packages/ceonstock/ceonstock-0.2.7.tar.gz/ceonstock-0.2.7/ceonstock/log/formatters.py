import logging
from ceonstock.log import formats
from enum import Enum

from .colors import TerminalColor


class ColoredFormatter(logging.Formatter):
    default_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def __init__(self, string_for_format: str, *args, **kwargs):
        self.msg_format = ColoredFormatter.default_format
        if string_for_format:
            self.msg_format = string_for_format
        # super().__init__(*args, **kwargs)

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
        # The color formatting must be applied to each line individually to take effect.
        colored_lines = []
        for line in formatted_msg.split("\n"):
            colored_line = f"{terminal_color.value}{line}{TerminalColor._RESET.value}"
            colored_lines.append(colored_line)
        colored_msg = "\n".join(colored_lines)
        return colored_msg

    def format(self, record):
        log_fmt = self.msg_format
        chosen_color = self.get_color(record.levelno)
        formatter = logging.Formatter(log_fmt)
        formatted_msg = formatter.format(record)
        colored_msg = self.apply_color(formatted_msg, chosen_color)
        return colored_msg


DEV = ColoredFormatter(formats.DEV)
# PROD = ColoredFormatter(formats.PROD)
PROD = logging.Formatter(formats.PROD)
