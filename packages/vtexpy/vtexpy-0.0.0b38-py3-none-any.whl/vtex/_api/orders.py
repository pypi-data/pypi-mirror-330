from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Union

from .._constants import (
    LIST_FEED_ORDERS_MAX_PAGE_SIZE,
    LIST_ORDERS_MAX_PAGE,
    LIST_ORDERS_MAX_PAGE_SIZE,
    LIST_ORDERS_START_PAGE,
    MIN_PAGE_SIZE,
)
from .._dto import VTEXDataResponse, VTEXItemsResponse, VTEXPaginatedItemsResponse
from .._sentinels import UNDEFINED, UndefinedSentinel
from .._types import OrderingDirectionType
from .._utils import now
from .base import BaseAPI


class OrdersAPI(BaseAPI):
    """
    Client for the Orders API.
    https://developers.vtex.com/docs/api-reference/orders-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def list_orders(
        self,
        query: Union[str, UndefinedSentinel] = UNDEFINED,
        search: Union[str, UndefinedSentinel] = UNDEFINED,
        creation_date_from: Union[datetime, UndefinedSentinel] = UNDEFINED,
        creation_date_to: Union[datetime, UndefinedSentinel] = UNDEFINED,
        incomplete: bool = False,
        order_by_field: str = "creationDate",
        order_by_direction: OrderingDirectionType = "DESC",
        page: int = LIST_ORDERS_START_PAGE,
        page_size: int = LIST_ORDERS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXPaginatedItemsResponse[Any, Any]:
        if page > LIST_ORDERS_MAX_PAGE:
            raise ValueError("List Orders endpoint can only return up to page 30")

        params: Dict[str, Union[str, int]] = {
            "incompleteOrders": incomplete,
            "orderBy": f"{order_by_field},{order_by_direction.lower()}",
            "page": max(
                min(page, LIST_ORDERS_MAX_PAGE),
                LIST_ORDERS_START_PAGE,
            ),
            "per_page": max(
                min(page_size, LIST_ORDERS_MAX_PAGE_SIZE),
                MIN_PAGE_SIZE,
            ),
            "_stats": 1,
        }

        if query is not UNDEFINED:
            params["q"] = str(query)

        if search is not UNDEFINED:
            params["searchField"] = str(search)

        if creation_date_from is not UNDEFINED or creation_date_to is not UNDEFINED:
            if not isinstance(creation_date_from, datetime):
                creation_date_from = self.client.custom.get_creation_date()

            if not isinstance(creation_date_to, datetime):
                creation_date_to = now() + timedelta(minutes=1)

            start = (
                creation_date_from.astimezone(timezone.utc)
                .replace(microsecond=0)
                .isoformat(timespec="milliseconds")
                .split("+")[0]
            )
            end = (
                creation_date_to.astimezone(timezone.utc)
                .replace(microsecond=999999)
                .isoformat(timespec="milliseconds")
                .split("+")[0]
            )

            params["f_creationDate"] = f"creationDate:[{start}Z TO {end}Z]"

        response = self._request(
            method="GET",
            endpoint="/api/oms/pvt/orders/",
            environment=self.ENVIRONMENT,
            params=params,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXPaginatedItemsResponse[Any, Any],
        )

        pagination = response.pagination
        if isinstance(pagination.next_page, int) and pagination.next_page > 30:
            pagination.next_page = None

        return response

    def get_order(self, order_id: str, **kwargs: Any) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/oms/pvt/orders/{order_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def list_feed_orders(
        self,
        page_size: int = LIST_FEED_ORDERS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXItemsResponse[Any, Any]:
        return self._request(
            method="GET",
            endpoint="/api/orders/feed/",
            environment=self.ENVIRONMENT,
            params={
                "maxlot": max(
                    min(page_size, LIST_FEED_ORDERS_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[Any, Any],
        )

    def commit_feed_orders(
        self,
        handles: List[str],
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        if not handles:
            raise ValueError(
                "At least one handle must be provided to commit to the feed"
            )
        elif len(handles) > LIST_FEED_ORDERS_MAX_PAGE_SIZE:
            raise ValueError(
                f"At most {LIST_FEED_ORDERS_MAX_PAGE_SIZE} feed orders can be commited"
                f"at once"
            )

        return self._request(
            method="POST",
            endpoint="/api/orders/feed/",
            environment=self.ENVIRONMENT,
            json={"handles": handles},
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )
