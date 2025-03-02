import logging
from pathlib import Path
from ceonstock.log import formatters

self_logger = logging.getLogger(__name__)


def file_handler(
    log_filepath: Path, formatter: logging.Formatter = formatters.PROD, level=None
):
    self_logger.info(f"Got log_filepath: {log_filepath}")
    log_dir = Path(log_filepath.parent)
    self_logger.debug(f"log_dir: {log_dir}")
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setFormatter(formatter)
    if level:
        file_handler.setLevel(level)
    return file_handler


def stream_handler(formatter: logging.Formatter = formatters.DEV, level=None):
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    if level:
        stream_handler.setLevel(level)
    return stream_handler


def create_dir(dir: Path):
    self_logger.debug(f"dir.exists(): {dir.exists()}")
    if not dir.exists():
        self_logger.info(f"Creating new folder(s): {dir}")
        dir.mkdir(parents=True, exist_ok=True)
    else:
        self_logger.info(f"dir already exists: {dir}")
