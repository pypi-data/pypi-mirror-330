from typing import Any

from .._dto import VTEXDataResponse
from .base import BaseAPI


class PricingAPI(BaseAPI):
    """
    Client for the Pricing API.
    https://developers.vtex.com/docs/api-reference/pricing-api
    """

    def get_price(self, sku_id: str, **kwargs: Any) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/pricing/prices/{sku_id}",
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )
