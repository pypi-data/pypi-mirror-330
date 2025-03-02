from . import _constants as VTEXConstants  # noqa: N812
from ._config import VTEXConfig
from ._dto import (
    VTEXCartItem,
    VTEXDataResponse,
    VTEXItemsResponse,
    VTEXPaginatedItemsResponse,
    VTEXResponse,
)
from ._exceptions import VTEXError, VTEXRequestError, VTEXResponseError
from ._vtex import VTEX

__all__ = [
    "VTEX",
    "VTEXCartItem",
    "VTEXConfig",
    "VTEXConstants",
    "VTEXError",
    "VTEXDataResponse",
    "VTEXItemsResponse",
    "VTEXPaginatedItemsResponse",
    "VTEXRequestError",
    "VTEXResponse",
    "VTEXResponseError",
]


for name in __all__:
    locals()[name].__module__ = "vtex"
