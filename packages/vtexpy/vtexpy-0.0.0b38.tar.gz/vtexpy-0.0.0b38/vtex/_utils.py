from datetime import datetime, timezone, tzinfo
from re import compile
from typing import Any, Dict, Mapping, Union
from uuid import UUID

from dateutil.parser import parse as parse_datetime
from dateutil.tz import tzoffset

from ._constants import APP_KEY_HEADER, APP_TOKEN_HEADER
from ._logging import UTILS_LOGGER
from ._sentinels import UNDEFINED

TO_SNAKE_CASE_STEP_1_PATTERN = compile(r"(.)([A-Z][a-z]+)")
TO_SNAKE_CASE_STEP_2_PATTERN = compile(r"([a-z0-9])([A-Z])")


def str_to_bool(value: str) -> bool:
    if isinstance(value, str):
        if value.lower() in {"true", "yes", "on", "y", "1"}:
            return True

        if value.lower() in {"false", "no", "off", "n", "0"}:
            return False

    raise ValueError(f"Invalid boolean repreentation: {value}")


def omitting_undefined(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    return {key: value for key, value in obj.items() if value is not UNDEFINED}


def remove_null_bytes(value: str) -> str:
    return value.replace("\x00", "")


def to_snake_case(string: str) -> str:
    string = remove_null_bytes(string)

    try:
        UUID(string)
    except (AttributeError, ValueError, TypeError):
        return TO_SNAKE_CASE_STEP_2_PATTERN.sub(
            r"\1_\2",
            TO_SNAKE_CASE_STEP_1_PATTERN.sub(r"\1_\2", string),
        ).lower()

    return string


def to_snake_case_deep(obj: Any) -> Any:
    if isinstance(obj, dict):
        snake_cased_obj = {}

        for key, value in sorted(obj.items(), key=lambda item: item[0]):
            if isinstance(key, str):
                key = to_snake_case(key)

                while key in snake_cased_obj:
                    UTILS_LOGGER.debug(
                        f"Snake cased key {key} appears multiple times in object",
                        extra={"object": obj, "key": key},
                    )
                    key = f"_{key}"

            snake_cased_obj[key] = to_snake_case_deep(value)

        return snake_cased_obj

    if isinstance(obj, (list, set, tuple)):
        return type(obj)([to_snake_case_deep(element) for element in obj])

    if isinstance(obj, str):
        return remove_null_bytes(obj)

    return obj


def to_tzinfo(tz: Union[tzinfo, int, None] = None) -> tzinfo:
    if isinstance(tz, tzinfo):
        return tz

    if isinstance(tz, int):
        return tzoffset(None, tz)

    return timezone.utc


def to_datetime(
    value: Union[datetime, str],
    use_tz: bool = True,
    tz: Union[tzinfo, int, None] = None,
) -> datetime:
    value_as_datetime = value if isinstance(value, datetime) else parse_datetime(value)

    if not use_tz:
        return value_as_datetime.replace(tzinfo=None)

    if value_as_datetime.tzinfo and tz is None:
        return value_as_datetime

    return value_as_datetime.replace(tzinfo=to_tzinfo(tz))


def now(use_tz: bool = True, tz: Union[tzinfo, None] = None) -> datetime:
    return datetime.now(to_tzinfo(tz) if use_tz else None)


def redact_headers(headers: Mapping[str, str]) -> Dict[str, str]:
    redacted_headers = {}

    for key, value in list(headers.items()):
        if key.lower() in {APP_KEY_HEADER.lower(), APP_TOKEN_HEADER.lower()}:
            redacted_headers[key] = "*" * 32
        else:
            redacted_headers[key] = value

    return redacted_headers


def join_url(base: str, *paths: str) -> str:
    return "/".join(part.strip("/") for part in [base, *paths])
