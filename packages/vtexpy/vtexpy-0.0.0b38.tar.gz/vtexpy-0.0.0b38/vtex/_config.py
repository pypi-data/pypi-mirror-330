from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from os import getenv
from typing import Any, List, Literal, Union

from pydantic import BaseModel, Field, SecretStr, field_validator

from ._constants import (
    ACCOUNT_NAME_ENV_VAR,
    APP_KEY_ENV_VAR,
    APP_TOKEN_ENV_VAR,
    DEFAULT_LOG_1XX,
    DEFAULT_LOG_2XX,
    DEFAULT_LOG_3XX,
    DEFAULT_LOG_4XX,
    DEFAULT_LOG_5XX,
    DEFAULT_LOG_RETRIES,
    DEFAULT_RAISE_FOR_STATUS_CODE,
    DEFAULT_RETRY_ATTEMPTS,
    DEFAULT_RETRY_BACKOFF_MAX,
    DEFAULT_RETRY_BACKOFF_MIN,
    DEFAULT_RETRY_STATUS_CODES,
    DEFAULT_TIMEOUT,
    LOG_1XX_ENV_VAR,
    LOG_2XX_ENV_VAR,
    LOG_3XX_ENV_VAR,
    LOG_4XX_ENV_VAR,
    LOG_5XX_ENV_VAR,
    LOG_RETRIES_ENV_VAR,
    RAISE_FOR_STATUS_CODE_ENV_VAR,
    RETRY_ATTEMPTS_ENV_VAR,
    RETRY_BACKOFF_MAX_ENV_VAR,
    RETRY_BACKOFF_MIN_ENV_VAR,
    RETRY_STATUS_CODES_ENV_VAR,
    TIMEOUT_ENV_VAR,
)
from ._sentinels import UNDEFINED, UndefinedSentinel
from ._types import LogLevelType
from ._utils import omitting_undefined, str_to_bool

FalseOrLogLevel = Union[Literal[False], LogLevelType]
FalseOrLogLevelOrUndefined = Union[FalseOrLogLevel, UndefinedSentinel]


class VTEXConfig(BaseModel):
    account_name: str = Field(  # type: ignore[assignment]
        UNDEFINED,
        validate_default=True,
    )
    app_key: SecretStr = Field(  # type: ignore[assignment]
        UNDEFINED,
        validate_default=True,
    )
    app_token: SecretStr = Field(  # type: ignore[assignment]
        UNDEFINED,
        validate_default=True,
    )

    timeout: Union[float, None] = Field(  # type: ignore[assignment]
        UNDEFINED,
        validate_default=True,
    )

    retry_attempts: int = Field(  # type: ignore[assignment]
        UNDEFINED,
        validate_default=True,
    )
    retry_backoff_min: float = Field(  # type: ignore[assignment]
        UNDEFINED,
        validate_default=True,
    )
    retry_backoff_max: float = Field(  # type: ignore[assignment]
        UNDEFINED,
        validate_default=True,
    )
    retry_status_codes: List[int] = Field(
        UNDEFINED,  # type: ignore[arg-type]
        validate_default=True,
    )

    raise_for_status_code: bool = Field(  # type: ignore[assignment]
        UNDEFINED,
        validate_default=True,
    )

    log_retries: FalseOrLogLevel = Field(
        UNDEFINED,
        validate_default=True,
    )
    log_1xx: FalseOrLogLevel = Field(
        UNDEFINED,
        validate_default=True,
    )
    log_2xx: FalseOrLogLevel = Field(
        UNDEFINED,
        validate_default=True,
    )
    log_3xx: FalseOrLogLevel = Field(
        UNDEFINED,
        validate_default=True,
    )
    log_4xx: FalseOrLogLevel = Field(
        UNDEFINED,
        validate_default=True,
    )
    log_5xx: FalseOrLogLevel = Field(
        UNDEFINED,
        validate_default=True,
    )

    def with_overrides(
        self,
        account_name: Union[str, UndefinedSentinel] = UNDEFINED,
        app_key: Union[SecretStr, str, UndefinedSentinel] = UNDEFINED,
        app_token: Union[SecretStr, str, UndefinedSentinel] = UNDEFINED,
        timeout: Union[float, int, None, UndefinedSentinel] = UNDEFINED,
        retry_attempts: Union[int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_min: Union[float, int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_max: Union[float, int, UndefinedSentinel] = UNDEFINED,
        retry_status_codes: Union[List[int], UndefinedSentinel] = UNDEFINED,
        raise_for_status_code: Union[bool, UndefinedSentinel] = UNDEFINED,
        log_retries: FalseOrLogLevelOrUndefined = UNDEFINED,
        log_1xx: FalseOrLogLevelOrUndefined = UNDEFINED,
        log_2xx: FalseOrLogLevelOrUndefined = UNDEFINED,
        log_3xx: FalseOrLogLevelOrUndefined = UNDEFINED,
        log_4xx: FalseOrLogLevelOrUndefined = UNDEFINED,
        log_5xx: FalseOrLogLevelOrUndefined = UNDEFINED,
    ) -> "VTEXConfig":
        return VTEXConfig(
            **{
                **self.model_dump(),
                **omitting_undefined({
                    "account_name": account_name,
                    "app_key": app_key,
                    "app_token": app_token,
                    "timeout": timeout,
                    "retry_attempts": retry_attempts,
                    "retry_backoff_min": retry_backoff_min,
                    "retry_backoff_max": retry_backoff_max,
                    "retry_status_codes": retry_status_codes,
                    "raise_for_status_code": raise_for_status_code,
                    "log_retries": log_retries,
                    "log_1xx": log_1xx,
                    "log_2xx": log_2xx,
                    "log_3xx": log_3xx,
                    "log_4xx": log_4xx,
                    "log_5xx": log_5xx,
                }),
            },
        )

    @field_validator("account_name", mode="before")
    @classmethod
    def validate_account_name(cls, value: Any) -> str:
        return cls._validate_required_string(value, ACCOUNT_NAME_ENV_VAR)

    @field_validator("app_key", mode="before")
    @classmethod
    def validate_app_key(cls, value: Any) -> str:
        return cls._validate_required_string(value, APP_KEY_ENV_VAR)

    @field_validator("app_token", mode="before")
    @classmethod
    def validate_app_token(cls, value: Any) -> str:
        return cls._validate_required_string(value, APP_TOKEN_ENV_VAR)

    @field_validator("timeout", mode="before")
    @classmethod
    def validate_timeout(cls, value: Any) -> Union[float, None]:
        if isinstance(value, UndefinedSentinel):
            value = getenv(TIMEOUT_ENV_VAR, DEFAULT_TIMEOUT)

        if isinstance(value, (str, float, int)):
            try:
                value = float(value)
            except ValueError:
                pass

            if isinstance(value, str) and value.lower() in {"", "none", "null"}:
                value = None

        if value is None or (isinstance(value, (float, int)) and value > 0):
            return value

        raise cls._prepare_value_error(value, TIMEOUT_ENV_VAR)

    @field_validator("retry_attempts", mode="before")
    @classmethod
    def validate_retry_attempts(cls, value: Any) -> int:
        if isinstance(value, UndefinedSentinel):
            value = getenv(RETRY_ATTEMPTS_ENV_VAR, DEFAULT_RETRY_ATTEMPTS)

        if isinstance(value, (str, int)):
            try:
                value = int(value)
            except ValueError:
                pass

        if isinstance(value, int) and value >= 0:
            return value

        raise cls._prepare_value_error(value, RETRY_ATTEMPTS_ENV_VAR)

    @field_validator("retry_backoff_min", mode="before")
    @classmethod
    def validate_retry_backoff_min(cls, value: Any) -> Union[float, int]:
        return cls._validate_number(
            value,
            RETRY_BACKOFF_MIN_ENV_VAR,
            DEFAULT_RETRY_BACKOFF_MIN,
            allow_zero=False,
        )

    @field_validator("retry_backoff_max", mode="before")
    @classmethod
    def validate_retry_backoff_max(cls, value: Any) -> Union[float, int]:
        return cls._validate_number(
            value,
            RETRY_BACKOFF_MAX_ENV_VAR,
            DEFAULT_RETRY_BACKOFF_MAX,
            allow_zero=False,
        )

    @field_validator("retry_status_codes", mode="before")
    @classmethod
    def validate_retry_status_codes(cls, value: Any) -> List[int]:
        if isinstance(value, UndefinedSentinel):
            value = getenv(RETRY_STATUS_CODES_ENV_VAR, DEFAULT_RETRY_STATUS_CODES)

        if isinstance(value, str):
            if value == "":
                value = []
            elif value == "*":
                value = list(range(100, 600))
            else:
                statuses = value.split(",")

                try:
                    value = [int(status.strip()) for status in statuses]
                except ValueError:
                    pass

        if isinstance(value, (list, set, tuple)) and all(
            isinstance(status, int) and 100 <= status <= 599 for status in value
        ):
            return list(value)

        raise cls._prepare_value_error(value, RETRY_STATUS_CODES_ENV_VAR)

    @field_validator("raise_for_status_code", mode="before")
    @classmethod
    def validate_raise_for_status_code(cls, value: Any) -> bool:
        if isinstance(value, UndefinedSentinel):
            value = getenv(RAISE_FOR_STATUS_CODE_ENV_VAR, DEFAULT_RAISE_FOR_STATUS_CODE)

        if isinstance(value, str):
            try:
                value = str_to_bool(value)
            except ValueError:
                pass

        if isinstance(value, bool):
            return value

        raise cls._prepare_value_error(value, RAISE_FOR_STATUS_CODE_ENV_VAR)

    @field_validator("log_retries", mode="before")
    @classmethod
    def validate_log_retries(cls, value: Any) -> FalseOrLogLevel:
        return cls._validate_false_or_loglevel(
            value,
            LOG_RETRIES_ENV_VAR,
            DEFAULT_LOG_RETRIES,
        )

    @field_validator("log_1xx", mode="before")
    @classmethod
    def validate_log_1xx(cls, value: Any) -> FalseOrLogLevel:
        return cls._validate_false_or_loglevel(
            value,
            LOG_1XX_ENV_VAR,
            DEFAULT_LOG_1XX,
        )

    @field_validator("log_2xx", mode="before")
    @classmethod
    def validate_log_2xx(cls, value: Any) -> FalseOrLogLevel:
        return cls._validate_false_or_loglevel(
            value,
            LOG_2XX_ENV_VAR,
            DEFAULT_LOG_2XX,
        )

    @field_validator("log_3xx", mode="before")
    @classmethod
    def validate_log_3xx(cls, value: Any) -> FalseOrLogLevel:
        return cls._validate_false_or_loglevel(
            value,
            LOG_3XX_ENV_VAR,
            DEFAULT_LOG_3XX,
        )

    @field_validator("log_4xx", mode="before")
    @classmethod
    def validate_log_4xx(cls, value: Any) -> FalseOrLogLevel:
        return cls._validate_false_or_loglevel(
            value,
            LOG_4XX_ENV_VAR,
            DEFAULT_LOG_4XX,
        )

    @field_validator("log_5xx", mode="before")
    @classmethod
    def validate_log_5xx(cls, value: Any) -> FalseOrLogLevel:
        return cls._validate_false_or_loglevel(
            value,
            LOG_5XX_ENV_VAR,
            DEFAULT_LOG_5XX,
        )

    @classmethod
    def _validate_required_string(cls, value: Any, env_var: str) -> str:
        if isinstance(value, UndefinedSentinel):
            value = getenv(env_var, UNDEFINED)

        if isinstance(value, SecretStr):
            value = value.get_secret_value()

        if isinstance(value, str) and value.strip():
            return value.strip()

        raise cls._prepare_value_error(value, env_var)

    @classmethod
    def _validate_number(
        cls,
        value: Any,
        env_var: str,
        default: Union[float, int],
        allow_zero: bool = False,
    ) -> float:
        if isinstance(value, UndefinedSentinel):
            value = getenv(env_var, default)

        if isinstance(value, (str, float, int)):
            try:
                value = float(value)
            except ValueError:
                pass

        if isinstance(value, (float, int)) and value >= 0 and (allow_zero or value > 0):
            return value

        raise cls._prepare_value_error(value, env_var)

    @classmethod
    def _validate_false_or_loglevel(
        cls,
        value: Any,
        env_var: str,
        default: FalseOrLogLevel,
    ) -> FalseOrLogLevel:
        if isinstance(value, UndefinedSentinel):
            value = getenv(env_var, default)

        if isinstance(value, str):
            try:
                value = str_to_bool(value)
            except ValueError:
                try:
                    value = int(value)
                except ValueError:
                    pass

        if value is False or value in {DEBUG, INFO, WARNING, ERROR, CRITICAL}:
            return value

        raise cls._prepare_value_error(value, env_var)

    @staticmethod
    def _prepare_value_error(value: Any, env_var: str) -> ValueError:
        error = "Missing" if isinstance(value, UndefinedSentinel) else "Invalid"
        field_name = env_var.lower().replace("vtex_", "")
        return ValueError(f"{error} {field_name}")
