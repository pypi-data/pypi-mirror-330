from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from sys import version_info
from typing import Literal

if version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

HTTPMethodType = Literal[
    "DELETE",
    "GET",
    "HEAD",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "delete",
    "get",
    "head",
    "options",
    "patch",
    "post",
    "put",
]

LogLevelType = Literal[  # type: ignore[valid-type]
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
]

OrderingDirectionType = Literal["ASC", "DESC", "asc", "desc"]

TypedDict = TypedDict
