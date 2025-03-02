from datetime import datetime
from typing import Any, List, Type, Union

from httpx._types import (
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
)

from .. import VTEXError
from .._dto import VTEXResponseType
from .._types import HTTPMethodType
from .._utils import to_datetime
from .base import BaseAPI
from .types.catalog import Seller
from .types.license_manager import AccountSite


class CustomAPI(BaseAPI):
    """
    Client for calling endpoints that have not yet been implemented by the SDK.
    You can directly call the `request` method to call any VTEX API.
    """

    def request(
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
        response_class: Union[Type[VTEXResponseType], None] = None,
        **kwargs: Any,
    ) -> VTEXResponseType:
        return self._request(
            method=method,
            endpoint=endpoint,
            environment=environment,
            headers=headers,
            cookies=cookies,
            params=params,
            json=json,
            data=data,
            content=content,
            files=files,
            config=self.client.config.with_overrides(**kwargs),
            response_class=response_class,
        )

    def get_account_name(self) -> str:
        return self.client.license_manager.get_account().data["account_name"]

    def get_creation_date(self) -> datetime:
        return to_datetime(
            self.client.license_manager.get_account().data["creation_date"],
        ).replace(hour=0, minute=0, second=0, microsecond=0)

    def list_sites(self) -> List[AccountSite]:
        return self.client.license_manager.get_account().data["sites"]

    def get_main_seller(self) -> Seller:
        for seller in self.client.catalog.list_sellers(seller_type=1).items:
            if seller["seller_id"] == "1":
                return seller

        raise VTEXError("Could not find main seller")

    def list_market_place_sellers(self, include_inactive: bool = False) -> List[Seller]:
        return [
            seller
            for seller in self.client.catalog.list_sellers(seller_type=1).items
            if (include_inactive or seller["is_active"]) and seller["seller_id"] != "1"
        ]

    def list_franchise_sellers(self, include_inactive: bool = False) -> List[Seller]:
        return [
            seller
            for seller in self.client.catalog.list_sellers(seller_type=2).items
            if include_inactive or seller["is_active"]
        ]
