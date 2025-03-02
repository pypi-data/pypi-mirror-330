from typing import Any

from .._constants import (
    LIST_CARRIERS_MAX_PAGE_SIZE,
    LIST_CARRIERS_START_PAGE,
    LIST_DOCKS_MAX_PAGE_SIZE,
    LIST_DOCKS_START_PAGE,
    LIST_SHIPPING_POLICIES_MAX_PAGE_SIZE,
    LIST_SHIPPING_POLICIES_START_PAGE,
    MIN_PAGE_SIZE,
)
from .._dto import VTEXDataResponse, VTEXItemsResponse, VTEXPaginatedItemsResponse
from .base import BaseAPI


class LogisticsAPI(BaseAPI):
    """
    Client for the Logistics API.
    https://developers.vtex.com/docs/api-reference/logistics-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def list_shipping_policies(
        self,
        page: int = LIST_SHIPPING_POLICIES_START_PAGE,
        page_size: int = LIST_SHIPPING_POLICIES_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXPaginatedItemsResponse[Any, Any]:
        return self._request(
            method="GET",
            endpoint="/api/logistics/pvt/shipping-policies",
            environment=self.ENVIRONMENT,
            params={
                "page": max(page, LIST_SHIPPING_POLICIES_START_PAGE),
                "perPage": max(
                    min(page_size, LIST_SHIPPING_POLICIES_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXPaginatedItemsResponse[Any, Any],
        )

    def get_shipping_policy(
        self,
        shipping_policy_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/logistics/pvt/shipping-policies/{shipping_policy_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def list_carriers(
        self,
        page: int = LIST_CARRIERS_START_PAGE,
        page_size: int = LIST_CARRIERS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXPaginatedItemsResponse[Any, Any]:
        return self._request(
            method="GET",
            endpoint="/api/logistics/pvt/configuration/carriers",
            environment=self.ENVIRONMENT,
            params={
                "page": max(page, LIST_CARRIERS_START_PAGE),
                "perPage": max(
                    min(page_size, LIST_CARRIERS_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXPaginatedItemsResponse[Any, Any],
        )

    def get_carrier(
        self,
        carrier_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/logistics/pvt/configuration/carriers/{carrier_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def list_docks(
        self,
        page: int = LIST_DOCKS_START_PAGE,
        page_size: int = LIST_DOCKS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXPaginatedItemsResponse[Any, Any]:
        return self._request(
            method="GET",
            endpoint="/api/logistics/pvt/configuration/docks",
            environment=self.ENVIRONMENT,
            params={
                "page": max(page, LIST_DOCKS_START_PAGE),
                "perPage": max(
                    min(page_size, LIST_DOCKS_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXPaginatedItemsResponse[Any, Any],
        )

    def get_dock(self, dock_id: str, **kwargs: Any) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/logistics/pvt/configuration/docks/{dock_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def list_carrier_freight_values(
        self,
        carrier_id: str,
        zip_code: str = "0",
        **kwargs: Any,
    ) -> VTEXItemsResponse[Any, Any]:
        return self._request(
            method="GET",
            endpoint=(
                f"/api/logistics/pvt/configuration/freights/{carrier_id}/{zip_code}"
                f"/values"
            ),
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[Any, Any],
        )

    def get_sku_inventories(
        self,
        sku_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/logistics/pvt/inventory/skus/{sku_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )
