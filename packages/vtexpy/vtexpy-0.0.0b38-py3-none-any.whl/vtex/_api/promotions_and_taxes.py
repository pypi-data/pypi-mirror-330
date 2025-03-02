from typing import Any

from .._dto import VTEXDataResponse, VTEXItemsResponse
from .base import BaseAPI


class PromotionsAndTaxesAPI(BaseAPI):
    """
    Client for the Promotions and Taxes API.
    https://developers.vtex.com/docs/api-reference/promotions-and-taxes-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def list_archived_promotions(
        self,
        **kwargs: Any,
    ) -> VTEXItemsResponse[Any, Any]:
        return self._request(
            method="GET",
            endpoint="api/rnb/pvt/archive/benefits/calculatorconfiguration",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[Any, Any],
        )

    def get_promotions(self, **kwargs: Any) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint="api/rnb/pvt/benefits/calculatorconfiguration",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def get_taxes(self, **kwargs: Any) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint="api/rnb/pvt/taxes/calculatorconfiguration",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def get_promotion_or_tax(
        self,
        promotion_or_tax_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/rnb/pvt/calculatorconfiguration/{promotion_or_tax_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )
