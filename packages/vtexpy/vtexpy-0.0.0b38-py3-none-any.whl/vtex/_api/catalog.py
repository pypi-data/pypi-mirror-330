from typing import Any, List, Union

from .._constants import (
    GET_CATEGORY_TREE_MAX_LEVELS,
    LIST_CATEGORIES_MAX_PAGE_SIZE,
    LIST_CATEGORIES_START_PAGE,
    LIST_SKU_IDS_MAX_PAGE_SIZE,
    LIST_SKU_IDS_START_PAGE,
    MIN_PAGE_SIZE,
)
from .._dto import VTEXDataResponse, VTEXItemsResponse, VTEXPaginatedItemsResponse
from .._sentinels import UNDEFINED, UndefinedSentinel
from .._utils import omitting_undefined
from .base import BaseAPI
from .types.catalog import SalesChannel, Seller


class CatalogAPI(BaseAPI):
    """
    Client for the Catalog API.
    https://developers.vtex.com/docs/api-reference/catalog-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def list_sellers(
        self,
        sales_channel: Union[int, UndefinedSentinel] = UNDEFINED,
        seller_type: Union[int, UndefinedSentinel] = UNDEFINED,
        is_better_scope: Union[bool, UndefinedSentinel] = UNDEFINED,
        **kwargs: Any,
    ) -> VTEXItemsResponse[List[Seller], Seller]:
        return self._request(
            method="GET",
            endpoint="/api/catalog_system/pvt/seller/list",
            environment=self.ENVIRONMENT,
            params=omitting_undefined({
                "sc": sales_channel,
                "sellerType": seller_type,
                "isBetterScope": is_better_scope,
            }),
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[Any, Any],
        )

    def list_sales_channels(
        self,
        **kwargs: Any,
    ) -> VTEXItemsResponse[List[SalesChannel], SalesChannel]:
        return self._request(
            method="GET",
            endpoint="/api/catalog_system/pvt/saleschannel/list",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[Any, Any],
        )

    def list_sku_ids(
        self,
        page: int = LIST_SKU_IDS_START_PAGE,
        page_size: int = LIST_SKU_IDS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXItemsResponse[List[int], int]:
        return self._request(
            method="GET",
            endpoint="/api/catalog_system/pvt/sku/stockkeepingunitids",
            environment=self.ENVIRONMENT,
            params={
                "page": max(page, LIST_SKU_IDS_START_PAGE),
                "pagesize": max(
                    min(page_size, LIST_SKU_IDS_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[List[int], int],
        )

    def get_sku_with_context(
        self,
        sku_id: int,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/catalog_system/pvt/sku/stockkeepingunitbyid/{sku_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def list_categories(
        self,
        page: int = LIST_SKU_IDS_START_PAGE,
        page_size: int = LIST_SKU_IDS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXPaginatedItemsResponse[Any, Any]:
        return self._request(
            method="GET",
            endpoint="/api/catalog/pvt/category",
            environment=self.ENVIRONMENT,
            params={
                "page": max(page, LIST_CATEGORIES_START_PAGE),
                "pagesize": max(
                    min(page_size, LIST_CATEGORIES_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXPaginatedItemsResponse[Any, Any],
        )

    def get_category_tree(
        self,
        levels: int = GET_CATEGORY_TREE_MAX_LEVELS,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/catalog_system/pub/category/tree/{levels}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def get_category(
        self,
        category_id: int,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/catalog/pvt/category/{category_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )
