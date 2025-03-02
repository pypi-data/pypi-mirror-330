from typing import Any, Dict, Union

from httpx import Headers


class VTEXError(Exception):
    def __init__(self, *args: Any, **kwags: Any) -> None:
        super().__init__(*args, **kwags)


class VTEXRequestError(VTEXError):
    def __init__(
        self,
        *args: Any,
        exception: Union[Exception, None] = None,
        method: Union[str, None] = None,
        url: Union[str, None] = None,
        headers: Union[Headers, Dict[str, str], None] = None,
        **kwargs: Any,
    ) -> None:
        self.args = args
        self.exception = exception
        self.method = method
        self.url = url
        self.headers = dict(headers) if headers else None
        self.kwargs = kwargs

        super().__init__(str(exception or "VTEXRequestError"), *args, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exception": self.exception,
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
        }


class VTEXResponseError(VTEXError):
    def __init__(
        self,
        *args: Any,
        method: Union[str, None] = None,
        url: Union[str, None] = None,
        request_headers: Union[Headers, Dict[str, str], None] = None,
        status_code: Union[int, None] = None,
        data: Any = None,
        response_headers: Union[Headers, Dict[str, str], None] = None,
        **kwargs: Any,
    ) -> None:
        self.args = args
        self.method = method
        self.url = url
        self.request_headers = dict(request_headers) if request_headers else None
        self.status_code = status_code
        self.data = data
        self.response_headers = dict(response_headers) if response_headers else None
        self.kwargs = kwargs

        super().__init__(str(data or "VTEXResponseError"), *args, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": self.method,
            "url": self.url,
            "request_headers": self.request_headers,
            "status_code": self.status_code,
            "data": self.data,
            "response_headers": self.response_headers,
        }
