from ..core import CstockJobType
from dataclass import dataclass
from enum import Enum
import errors


class CstockRenderFPS(Enum):
    FPS_24 = 24
    FPS_25 = 24
    FPS_30 = 30
    FPS_50 = 50
    FPS_60 = 60


@dataclass
class RenderResolution:
    width: int
    height: int

    @classmethod
    def from_string(cls, string: str):
        parsed_string = string.lower().split("x")
        if len(parsed_string) == 2:
            width = int(parsed_string[0])
            height = int(parsed_string[1])
            return cls(width, height)
        raise Exception(
            f"Failed to parse string '{string}' for RenderRsolution.from_string()"
        )

    def __str__(self):
        return f"{self.width}x{self.height}"


class CstockRenderSettings():
    resolution: RenderResolution
    framerate: int
    watermarked: bool

    def __str__(self):
        # return f"<ProjInputType '{self.name}'>"
        return f"<{self.__class__.__name__}>"


DEFAULT_FRAMERATE = CstockRenderFPS.FPS_30

RENDER_PREVIEW = CstockRenderSettings(
    resolution=RenderResolution(480, 270),
    framerate=DEFAULT_FRAMERATE,
    watermarked=True
)
RENDER_STANDARD = CstockRenderSettings(
    resolution=RenderResolution(1920, 1080),
    framerate=DEFAULT_FRAMERATE,
    watermarked=False
)
RENDER_PRODUCTION = CstockRenderSettings(
    resolution=RenderResolution(3840, 2160),
    framerate=DEFAULT_FRAMERATE,
    watermarked=False
)


def default_render_settings(job_type: CstockJobType):
    CLASS_LOOKUP = {
        CstockJobType.PREVIEW: RENDER_PREVIEW,
        CstockJobType.STANDARD: RENDER_STANDARD,
        CstockJobType.PRODUCTION: RENDER_PRODUCTION
    }
    try:
        type_class = CLASS_LOOKUP[job_type]
    except KeyError:
        raise errors.UnknownJobTypeException(job_type)
    return type_class

