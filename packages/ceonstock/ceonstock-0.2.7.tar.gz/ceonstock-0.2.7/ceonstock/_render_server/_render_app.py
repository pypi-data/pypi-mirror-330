from dataclasses import dataclass
from typing import Optional
from abc import ABC
# from dataclasses import dataclass
from enum import Enum

from typing import Optional, Type, Dict, TypeVar
from ceonstock.log import create_new_logger
from .. import errors

logger = create_new_logger(__name__)

# P = TypeVar("P", bound="ICstockRenderAppSettings")

class CstockRenderAppType(Enum):
    HOU = "hou"
    FFMPEG = "ffmpeg"
    NUKE = "nuke"

    # def get_class(self):
    # return get_app_settings_cls(self)

    # def make_app_settings(self, kwargs=None):
    # return make_app_settings(self, kwargs)


class RenderEngineType(Enum):
    MANTRA = "mantra"  # Houdini old engine
    KARMA = "karma"  # Houdini new engine
    REDSHIFT = "redshift"  # Redshift


# For type hinting/ide to recognize inherited classes
class ICstockRenderAppSettings(ABC):
    pass

# -- App Settings classes--
# Contains settings which are required to execute a render in the target app.
# --


@dataclass
class CstockRenderAppSettingsFFmpeg(ICstockRenderAppSettings):
    input_args: str
    output_args: str


@dataclass
class CstockRenderAppSettingsHou(ICstockRenderAppSettings):
    target_node: str
    nodetype: str
    frames: str
    render_engine: Optional[RenderEngineType] = None
    take: str = "Main"


def get_app_settings_cls(
    app: CstockRenderAppType,
) -> Type[ICstockRenderAppSettings]:
    CLASS_LOOKUP = {
        CstockRenderAppType.HOU: CstockRenderAppSettingsHou,
        CstockRenderAppType.FFMPEG: CstockRenderAppSettingsFFmpeg,
    }
    try:
        type_class = CLASS_LOOKUP[app]
    except KeyError:
        raise errors.UnknownRenderAppTypeError(app)
    return type_class


def make_app_settings(
    app: CstockRenderAppType, kwargs: Optional[Dict] = None
) -> ICstockRenderAppSettings:
    if not kwargs:
        kwargs = {}
    app_settings_cls = get_app_settings_cls(app)
    logger.debug(f"Creating {app_settings_cls} with kwargs: ", kwargs)
    app_settings = app_settings_cls(**kwargs)
    logger.debug(f"Created instance: {app_settings}")
    return app_settings
