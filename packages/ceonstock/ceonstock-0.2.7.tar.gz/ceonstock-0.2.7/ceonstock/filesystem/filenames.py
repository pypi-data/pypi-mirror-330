# A module to handle converting filename formats between different contexts.
# For example, Houdini uses $F3 to denote 3 digits, while regex uses (TODO what is the regex equiv?)
import logging

logger = logging.getLogger(__name__)


def hou_to_ffmpeg(filename: str):
    replaced = filename.replace("$F", "%0")
    logger.info(f"{filename=}")
    logger.info(f"{replaced=}")

    # Add the 'd' found in ffmpeg glob sysntax
    logger.warning(f"TODO: Use globbing to handle cases where %04d is not 4")
    replaced = replaced.replace("%04", "%04d")

    return replaced


def ffmpeg_to_hou(filename: str):
    replaced = filename.replace("%0", "$F")
    logger.info(f"{filename=}")
    logger.info(f"{replaced=}")
    return replaced
