from typing import Any, List, Union

from .._dto import VTEXCartItem, VTEXDataResponse
from .._sentinels import UNDEFINED, UndefinedSentinel
from .._utils import omitting_undefined
from .base import BaseAPI


class CheckoutAPI(BaseAPI):
    """
    Client for the Catalog API.
    https://developers.vtex.com/docs/api-reference/checkout-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def run_cart_simulation(
        self,
        cart: List[VTEXCartItem],
        country: Union[str, UndefinedSentinel] = UNDEFINED,
        postal_code: Union[str, UndefinedSentinel] = UNDEFINED,
        geo_coordinates: Union[List[float], UndefinedSentinel] = UNDEFINED,
        rnb_behavior: Union[int, UndefinedSentinel] = UNDEFINED,
        sales_channel: Union[int, UndefinedSentinel] = UNDEFINED,
        individual_shipping_estimates: Union[bool, UndefinedSentinel] = UNDEFINED,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="POST",
            endpoint="/api/checkout/pub/orderForms/simulation",
            environment=self.ENVIRONMENT,
            params=omitting_undefined({
                "RnbBehavior": rnb_behavior,
                "sc": sales_channel,
                "individualShippingEstimates": individual_shipping_estimates,
            }),
            json=omitting_undefined({
                "items": [item.to_vtex_cart_item() for item in cart],
                "country": country,
                "postalCode": postal_code,
                "geoCoordinates": geo_coordinates,
            }),
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )
