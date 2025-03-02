from functools import cached_property
from typing import TYPE_CHECKING, Any

from ._config import VTEXConfig
from ._logging import CLIENT_LOGGER

if TYPE_CHECKING:
    from ._api import (
        CatalogAPI,
        CheckoutAPI,
        CustomAPI,
        LicenseManagerAPI,
        LogisticsAPI,
        MasterDataAPI,
        OrdersAPI,
        PaymentsGatewayAPI,
        PricingAPI,
        PromotionsAndTaxesAPI,
    )


class VTEX:
    """
    Entrypoint for the VTEX SDK.
    From this class you can access all the APIs on VTEX
    """

    def __init__(self, config: VTEXConfig) -> None:
        self.logger = CLIENT_LOGGER
        self.config = config

    def with_config_overrides(self, **kwargs: Any) -> "VTEX":
        if not kwargs:
            return self

        return VTEX(config=self.config.with_overrides(**kwargs))

    @cached_property
    def custom(self) -> "CustomAPI":
        from ._api import CustomAPI

        return CustomAPI(client=self)

    @cached_property
    def catalog(self) -> "CatalogAPI":
        from ._api import CatalogAPI

        return CatalogAPI(client=self)

    @cached_property
    def checkout(self) -> "CheckoutAPI":
        from ._api import CheckoutAPI

        return CheckoutAPI(client=self)

    @cached_property
    def license_manager(self) -> "LicenseManagerAPI":
        from ._api import LicenseManagerAPI

        return LicenseManagerAPI(client=self)

    @cached_property
    def logistics(self) -> "LogisticsAPI":
        from ._api import LogisticsAPI

        return LogisticsAPI(client=self)

    @cached_property
    def master_data(self) -> "MasterDataAPI":
        from ._api import MasterDataAPI

        return MasterDataAPI(client=self)

    @cached_property
    def orders(self) -> "OrdersAPI":
        from ._api import OrdersAPI

        return OrdersAPI(client=self)

    @cached_property
    def pricing(self) -> "PricingAPI":
        from ._api import PricingAPI

        return PricingAPI(client=self)

    @cached_property
    def payments_gateway(self) -> "PaymentsGatewayAPI":
        from ._api import PaymentsGatewayAPI

        return PaymentsGatewayAPI(client=self)

    @cached_property
    def promotions_and_taxes(self) -> "PromotionsAndTaxesAPI":
        from ._api import PromotionsAndTaxesAPI

        return PromotionsAndTaxesAPI(client=self)
