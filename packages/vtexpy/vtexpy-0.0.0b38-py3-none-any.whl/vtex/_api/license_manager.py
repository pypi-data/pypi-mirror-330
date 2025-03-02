from typing import Any, List, Union

from cachetools import TTLCache, cached

from .._constants import (
    HOUR,
    LIST_ROLES_MAX_PAGE_SIZE,
    LIST_ROLES_START_PAGE,
    MIN_PAGE_SIZE,
)
from .._dto import VTEXDataResponse, VTEXItemsResponse, VTEXPaginatedItemsResponse
from .._sentinels import UNDEFINED, UndefinedSentinel
from .._types import OrderingDirectionType
from .base import BaseAPI
from .types.license_manager import GetAccountData, ListRolesData, Role, UserRole


class LicenseManagerAPI(BaseAPI):
    """
    Client for the License Manager API.
    https://developers.vtex.com/docs/api-reference/license-manager-api
    """

    ENVIRONMENT = "vtexcommercestable"

    @cached(TTLCache(maxsize=1024, ttl=HOUR))
    def get_account(self, **kwargs: Any) -> VTEXDataResponse[GetAccountData]:
        return self._request(
            method="GET",
            endpoint="/api/vlm/account",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[GetAccountData],
        )

    def get_user_roles(
        self,
        user_id: Union[str, UndefinedSentinel] = UNDEFINED,
        **kwargs: Any,
    ) -> VTEXItemsResponse[List[UserRole], UserRole]:
        config = self.client.config.with_overrides(**kwargs)

        if not user_id:
            app_keys = {
                app_key["app_key"]: app_key
                for app_key in self.get_account().data["app_keys"]
            }

            user_id = app_keys[config.app_key.get_secret_value()]["id"]

        return self._request(
            method="GET",
            endpoint=f"/api/license-manager/users/{user_id}/roles",
            environment=self.ENVIRONMENT,
            config=config,
            response_class=VTEXItemsResponse[List[UserRole], UserRole],
        )

    def list_roles(
        self,
        order_by_field: str = "id",
        order_by_direction: OrderingDirectionType = "DESC",
        page: int = LIST_ROLES_START_PAGE,
        page_size: int = LIST_ROLES_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXPaginatedItemsResponse[ListRolesData, Role]:
        return self._request(
            method="GET",
            endpoint="/api/license-manager/site/pvt/roles/list/paged",
            environment=self.ENVIRONMENT,
            params={
                "sort": order_by_field,
                "sortType": order_by_direction,
                "pageNumber": max(page, LIST_ROLES_START_PAGE),
                "numItems": max(
                    min(page_size, LIST_ROLES_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXPaginatedItemsResponse[ListRolesData, Role],
        )
