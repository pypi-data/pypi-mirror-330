from ceonstock.core.base import CstockBaseEnum


class CstockWebInputType(CstockBaseEnum):
    AUDIO = "audio"
    BOOL = "bool"
    COLOR = "color"
    DOC = "doc"  # Convert docs to imgs
    DROPDOWN = "dropdown"
    IMG = "img"
    INT = "int"
    TEXT = "text"


# TODO move metadata / info modules elsewhere
# @dataclass(frozen=True)
# class WebInputTypeInfo:
#     """Information about a particular CstockWebInputType which does NOT change per-instance"""

#     job_input_type: job_input.CstockJobInputType
#     is_file: bool = False


# def get_info(web_input_type: CstockWebInputType):
#     LOOKUP = {
#         CstockWebInputType.AUDIO: WebInputTypeInfo(
#             job_input_type=job_input.CstockJobInputType.AUDIO,
#             is_file=True,
#         ),
#         CstockWebInputType.COLOR: WebInputTypeInfo(
#             job_input_type=job_input.CstockJobInputType.COLOR,
#         ),
#         CstockWebInputType.DOC: WebInputTypeInfo(
#             job_input_type=job_input.CstockJobInputType.IMG,
#             is_file=True,
#         ),
#         CstockWebInputType.IMG: WebInputTypeInfo(
#             job_input_type=job_input.CstockJobInputType.IMG,
#             is_file=True,
#         ),
#     }
#     try:
#         type_class = LOOKUP[web_input_type]
#     except KeyError:
#         raise errors.CstockUnknownTypeError(
#             received=web_input_type, expected=CstockWebInputType
#         )
#     return type_class
