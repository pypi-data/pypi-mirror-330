from contextlib import contextmanager
from logging import CRITICAL, Logger, getLogger
from typing import Any, Callable, Generator, List, Union

from httpx import HTTPStatusError
from tenacity import RetryCallState


def get_logger(name: str, parent: Union[Logger, None] = None) -> Logger:
    if parent:
        return parent.getChild(name)

    return getLogger(f"vtex.{name}")


@contextmanager
def disable_loggers(logger_names: List[str]) -> Generator[None, None, None]:
    current_log_levels = {}

    for logger_name in logger_names:
        logger = getLogger(logger_name)
        current_log_levels[logger_name] = logger.level

        logger.setLevel(CRITICAL)

    try:
        yield
    finally:
        for logger_name, log_level in current_log_levels.items():
            getLogger(logger_name).setLevel(log_level)


def log_before_retry(
    logger: Logger,
    log_level: int,
    **kwargs: Any,
) -> Callable[[RetryCallState], None]:
    def retry_log(retry_state: RetryCallState) -> None:
        if not retry_state.outcome or not retry_state.next_action:
            raise RuntimeError("Retry log called before request was finished")

        exception = retry_state.outcome.exception()
        if not isinstance(exception, HTTPStatusError):
            raise RuntimeError("Retry log called without an http status error outcome")

        method = str(exception.request.method)
        url = str(exception.request.url)
        status_code = str(exception.response.status_code)
        reason = str(exception.response.reason_phrase)

        logger.log(
            log_level,
            f"Retrying {method} {url} in {retry_state.next_action.sleep}s as "
            f"attempt {retry_state.attempt_number} failed with: {status_code} {reason}",
            extra={
                "exception": exception,
                "attempt": retry_state.attempt_number,
                "sleep": retry_state.next_action.sleep,
                "method": method,
                "url": url,
                "status_code": status_code,
                **kwargs,
            },
        )

    return retry_log


CLIENT_LOGGER = get_logger(name="client")
EXCEPTIONS_LOGGER = get_logger(name="exceptions")
UTILS_LOGGER = get_logger(name="utils")
