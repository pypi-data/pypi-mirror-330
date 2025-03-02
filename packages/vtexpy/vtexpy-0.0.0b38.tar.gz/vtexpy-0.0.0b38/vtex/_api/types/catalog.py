from typing import Union

from ..._types import TypedDict


class Seller(TypedDict):
    fulfillment_seller_id: Union[str, None]
    is_active: bool
    is_better_scope: bool
    merchant_name: Union[str, None]
    name: str
    seller_id: str
    seller_type: int


class SalesChannel(TypedDict):
    id: int
    is_active: bool
    name: str
    position: Union[int, None]
    time_zone: str
