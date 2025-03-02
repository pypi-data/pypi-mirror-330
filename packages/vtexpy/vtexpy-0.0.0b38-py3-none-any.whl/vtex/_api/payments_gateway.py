from typing import Any

from .._dto import VTEXDataResponse, VTEXItemsResponse
from .base import BaseAPI


class PaymentsGatewayAPI(BaseAPI):
    """
    Client for the Payments Gateway API.
    https://developers.vtex.com/docs/api-reference/payments-gateway-api
    """

    ENVIRONMENT = "vtexpayments"

    def get_transaction(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/pvt/transactions/{transaction_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def list_transaction_interactions(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXItemsResponse[Any, Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/pvt/transactions/{transaction_id}/interactions",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[Any, Any],
        )

    def list_transaction_payments(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXItemsResponse[Any, Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/pvt/transactions/{transaction_id}/payments",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[Any, Any],
        )

    def get_transaction_payment(
        self,
        transaction_id: str,
        payment_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/pvt/transactions/{transaction_id}/payments/{payment_id}",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def get_transaction_capabilities(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/pvt/transactions/{transaction_id}/capabilities",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def get_transaction_cancellations(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/pvt/transactions/{transaction_id}/cancellations",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def get_transaction_refunds(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/pvt/transactions/{transaction_id}/refunds",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )

    def get_transaction_settlements(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=f"/api/pvt/transactions/{transaction_id}/settlements",
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )
