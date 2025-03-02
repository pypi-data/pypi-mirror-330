from typing import Any, List, Union

from .._constants import (
    MIN_PAGE_SIZE,
    SEARCH_DOCUMENTS_MAX_PAGE_SIZE,
    SEARCH_DOCUMENTS_START_PAGE,
)
from .._dto import VTEXPaginatedItemsResponse
from .._sentinels import UNDEFINED, UndefinedSentinel
from .._types import OrderingDirectionType
from .._utils import omitting_undefined
from .base import BaseAPI


class MasterDataAPI(BaseAPI):
    """
    Client for the Master Data API.
    https://developers.vtex.com/docs/api-reference/master-data-api-v2
    """

    ENVIRONMENT = "vtexcommercestable"

    def list_documents(
        self,
        entity_name: str,
        where: Union[str, UndefinedSentinel] = UNDEFINED,
        fields: Union[List[str], str, UndefinedSentinel] = UNDEFINED,
        order_by_field: str = "id",
        order_by_direction: OrderingDirectionType = "DESC",
        page: int = SEARCH_DOCUMENTS_START_PAGE,
        page_size: int = SEARCH_DOCUMENTS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXPaginatedItemsResponse[Any, Any]:
        params = {
            "_where": where,
            "_sort": f"{order_by_field} {order_by_direction.upper()}",
        }

        if fields is UNDEFINED:
            params["_fields"] = "all"
        elif not isinstance(fields, str) and isinstance(fields, list):
            params["_fields"] = ",".join(fields)
        else:
            params["_fields"] = fields

        page = max(page, SEARCH_DOCUMENTS_START_PAGE)
        page_size = max(
            min(page_size, SEARCH_DOCUMENTS_MAX_PAGE_SIZE),
            MIN_PAGE_SIZE,
        )

        return self._request(
            method="GET",
            endpoint=f"/api/dataentities/{entity_name}/search",
            environment=self.ENVIRONMENT,
            params=omitting_undefined(params),
            headers={
                "REST-Range": f"resources={(page - 1) * page_size}-{page * page_size}",
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXPaginatedItemsResponse[Any, Any],
        )
