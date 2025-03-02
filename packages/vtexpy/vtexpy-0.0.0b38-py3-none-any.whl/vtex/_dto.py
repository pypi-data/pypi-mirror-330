from json import JSONDecodeError
from math import ceil
from typing import Any, Dict, Generic, List, TypeVar, Union

from httpx import Request, Response
from pydantic import BaseModel, ConfigDict

from ._utils import remove_null_bytes, to_snake_case_deep

VTEXResponseType = TypeVar("VTEXResponseType", bound="VTEXResponse")
DataType = TypeVar("DataType", bound=Any)
ItemType = TypeVar("ItemType", bound=Any)


class VTEXRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    request: Request
    method: str
    url: str
    headers: Dict[str, str]

    @classmethod
    def factory(cls, request: Request) -> "VTEXRequest":
        return cls(
            request=request,
            method=str(request.method).upper(),
            url=str(request.url),
            headers=dict(request.headers),
        )


class VTEXResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    request: VTEXRequest
    response: Response
    status_code: int
    headers: Dict[str, str]

    @classmethod
    def factory(cls, response: Response) -> "VTEXResponse":
        return cls(
            request=VTEXRequest.factory(response.request),
            response=response,
            status_code=int(response.status_code),
            headers=dict(response.headers),
        )


class VTEXDataResponse(VTEXResponse, Generic[DataType]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: DataType

    @classmethod
    def get_original_response_data(cls, response: Response) -> Any:
        try:
            return to_snake_case_deep(response.json(strict=False))
        except JSONDecodeError:
            return remove_null_bytes(response.text)

    @classmethod
    def factory(cls, response: Response) -> "VTEXDataResponse[DataType]":
        vtex_response = VTEXResponse.factory(response)

        return cls(
            request=vtex_response.request,
            response=vtex_response.response,
            status_code=vtex_response.status_code,
            headers=vtex_response.headers,
            data=cls.get_original_response_data(response),
        )


class VTEXItemsResponse(VTEXDataResponse[DataType], Generic[DataType, ItemType]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    items: List[ItemType]

    @classmethod
    def factory(cls, response: Response) -> "VTEXItemsResponse[DataType, ItemType]":
        vtex_data_response = VTEXDataResponse[DataType].factory(response)
        data = vtex_data_response.data

        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and isinstance(data.get("list"), list):
            items = data["list"]
        elif isinstance(data, dict) and isinstance(data.get("items"), list):
            items = data["items"]
        elif isinstance(data, dict) and isinstance(data.get("data"), list):
            items = data["data"]
        else:
            raise ValueError(f"Not a valid items response: {data}")

        return cls(
            request=vtex_data_response.request,
            response=vtex_data_response.response,
            status_code=vtex_data_response.status_code,
            headers=vtex_data_response.headers,
            data=vtex_data_response.data,
            items=list(items),
        )


class VTEXPagination(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    total: int
    pages: int
    page_size: int
    page: int
    previous_page: Union[int, None]
    next_page: Union[int, None]

    @classmethod
    def factory(
        cls,
        vtex_items_response: VTEXItemsResponse[DataType, ItemType],
    ) -> "VTEXPagination":
        data = vtex_items_response.data
        request_headers = vtex_items_response.request.headers
        response_headers = vtex_items_response.headers

        total, pages, page_size, page = -1, -1, -1, -1
        if isinstance(data, dict) and data.get("paging"):
            pagination = data["paging"]
            total = pagination["total"]
            page_size = pagination["per_page"]
            pages = pagination["pages"]
            page = int(pagination.get("page") or pagination.get("current_page"))
        elif isinstance(data, dict) and data.get("total_page"):
            total = data["total_rows"]
            page_size = data["size"]
            pages = data["total_page"]
            page = data["page"]
        elif "rest-content-range" in response_headers:
            request_pagination = request_headers["rest-range"].split("=")[-1].split("-")
            response_pagination = response_headers["rest-content-range"].split(" ")[-1]
            total = int(response_pagination.split("/")[1])
            page_size = int(request_pagination[1]) - int(request_pagination[0])
            pages = ceil(total / page_size)
            page = ceil(
                int(response_pagination.split("/")[0].split("-")[1]) / page_size
            )

        if all(
            isinstance(field, int) and field != -1
            for field in {total, pages, page_size, page}
        ):
            return cls(
                total=total,
                pages=pages,
                page_size=page_size,
                page=page,
                previous_page=page - 1 if page > 1 else None,
                next_page=page + 1 if page < pages else None,
            )

        raise ValueError(f"Not a valid paginated items response: {vtex_items_response}")


class VTEXPaginatedItemsResponse(VTEXItemsResponse[DataType, ItemType]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pagination: VTEXPagination

    @classmethod
    def factory(cls, response: Response) -> "VTEXItemsResponse[DataType, ItemType]":
        vtex_items_response = VTEXItemsResponse[DataType, ItemType].factory(response)

        return cls(
            request=vtex_items_response.request,
            response=vtex_items_response.response,
            data=vtex_items_response.data,
            status_code=vtex_items_response.status_code,
            headers=vtex_items_response.headers,
            items=vtex_items_response.items,
            pagination=VTEXPagination.factory(vtex_items_response),
        )


class VTEXCartItem(BaseModel):
    seller_id: str
    sku_id: Union[int, str]
    quantity: int

    def to_vtex_cart_item(self) -> Dict[str, Any]:
        return {
            "seller": self.seller_id,
            "id": str(self.sku_id),
            "quantity": self.quantity,
        }
