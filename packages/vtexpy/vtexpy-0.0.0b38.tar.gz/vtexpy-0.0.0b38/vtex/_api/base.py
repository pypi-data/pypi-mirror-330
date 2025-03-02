from http import HTTPStatus
from json import JSONDecodeError
from typing import Any, Type, Union, cast

from httpx import (
    Client,
    Headers,
    HTTPError,
    HTTPStatusError,
    Response,
)
from httpx._types import (
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
)
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .._config import VTEXConfig
from .._constants import APP_KEY_HEADER, APP_TOKEN_HEADER
from .._dto import VTEXDataResponse, VTEXResponseType
from .._exceptions import VTEXRequestError, VTEXResponseError
from .._logging import disable_loggers, get_logger, log_before_retry
from .._types import HTTPMethodType
from .._utils import join_url, redact_headers, to_snake_case, to_snake_case_deep
from .._vtex import VTEX


class BaseAPI:
    """
    Base client for a VTEX API.
    """

    def __init__(self, client: VTEX) -> None:
        self.client = client
        self.logger = get_logger(
            name=to_snake_case(type(self).__name__),
            parent=self.client.logger,
        )

    def _request(  # noqa: C901
        self,
        method: HTTPMethodType,
        endpoint: str,
        environment: Union[str, None] = None,
        headers: Union[HeaderTypes, None] = None,
        cookies: Union[CookieTypes, None] = None,
        params: Union[QueryParamTypes, None] = None,
        json: Union[Any, None] = None,
        data: Union[RequestData, None] = None,
        content: Union[RequestContent, None] = None,
        files: Union[RequestFiles, None] = None,
        config: Union[VTEXConfig, None] = None,
        response_class: Union[Type[VTEXResponseType], None] = None,
        **kwargs: Any,
    ) -> VTEXResponseType:
        request_config = (config or self.client.config).with_overrides(**kwargs)

        if environment:
            url = join_url(
                f"https://{request_config.account_name}.{environment}.com.br",
                endpoint,
            )
        else:
            url = join_url(
                "https://api.vtex.com/",
                request_config.account_name,
                endpoint,
            )

        headers = Headers(headers=headers)
        headers[APP_KEY_HEADER] = request_config.app_key.get_secret_value()
        headers[APP_TOKEN_HEADER] = request_config.app_token.get_secret_value()
        headers["Content-Type"] = "application/json; charset=utf-8"
        headers["Accept"] = "application/json"

        @retry(
            stop=stop_after_attempt(
                max_attempt_number=request_config.retry_attempts + 1,
            ),
            wait=wait_exponential(
                min=request_config.retry_backoff_min,
                max=request_config.retry_backoff_max,
                exp_base=2.0,
            ),
            retry=retry_if_exception_type(exception_types=HTTPStatusError),
            before_sleep=(
                log_before_retry(
                    logger=self.logger,
                    log_level=request_config.log_retries,
                    environment=environment,
                    endpoint=endpoint,
                    account_name=request_config.account_name,
                )
                if request_config.log_retries is not False
                else None
            ),
            reraise=True,
        )
        def send_vtex_request() -> Response:
            with Client(timeout=request_config.timeout) as client:
                with disable_loggers(["httpcore", "httpx"]):
                    response = client.request(
                        method.upper(),
                        url,
                        headers=headers,
                        cookies=cookies,
                        params=params,
                        json=json,
                        data=data,
                        content=content,
                        files=files,
                    )

                response.request.headers = Headers(
                    redact_headers(dict(response.request.headers)),
                )
                response.headers = Headers(redact_headers(dict(response.headers)))

                for should_log, log_level in [
                    (response.is_informational, request_config.log_1xx),
                    (response.is_success, request_config.log_2xx),
                    (response.is_redirect, request_config.log_3xx),
                    (response.is_client_error, request_config.log_4xx),
                    (response.is_server_error, request_config.log_5xx),
                ]:
                    if should_log and log_level:
                        self.logger.log(
                            log_level,
                            f"{response.request.method} {response.request.url} "
                            f"{response.status_code} {response.reason_phrase}",
                            extra={
                                "method": response.request.method,
                                "url": response.request.url,
                                "status_code": response.status_code,
                                "environment": environment,
                                "endpoint": endpoint,
                                "account_name": request_config.account_name,
                            },
                        )

                if response.status_code in request_config.retry_status_codes:
                    response.raise_for_status()

                return response

        try:
            response = send_vtex_request()
        except HTTPStatusError as exception:
            response = exception.response
        except HTTPError as exception:
            headers = redact_headers(dict(headers))

            details = {
                "exception": exception,
                "method": str(method).upper(),
                "url": str(url),
                "headers": headers,
            }

            self.logger.error(str(exception), extra=details, exc_info=True)

            raise VTEXRequestError(**details) from None  # type: ignore[arg-type]

        self._raise_from_response(response=response, config=request_config)

        return cast(
            VTEXResponseType,
            (response_class or VTEXDataResponse).factory(response),
        )

    def _raise_from_response(self, response: Response, config: VTEXConfig) -> None:
        if response.is_error and config.raise_for_status_code:
            try:
                data = to_snake_case_deep(response.json(strict=False))
            except JSONDecodeError:
                data = response.text or HTTPStatus(response.status_code).phrase

            raise VTEXResponseError(
                data,
                method=str(response.request.method).upper(),
                url=str(response.request.url),
                request_headers=response.request.headers,
                status_code=response.status_code,
                data=data,
                response_headers=response.headers,
            ) from None
