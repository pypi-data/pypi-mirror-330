from typing import List, Union

from ..._types import TypedDict
from .generic import PagePagination


class AccountAppKey(TypedDict):
    app_key: str
    id: str
    is_active: bool
    is_blocked: bool
    label: str


class AccountSite(TypedDict):
    name: str


class GetAccountData(TypedDict):
    account_name: str
    app_keys: List[AccountAppKey]
    company_name: str
    creation_date: str
    have_parent_account: bool
    id: str
    inactivation_date: Union[str, None]
    is_active: bool
    is_operating: bool
    name: str
    operation_date: Union[str, None]
    parent_account_id: Union[str, None]
    parent_account_name: Union[str, None]
    sites: List[AccountSite]
    trading_name: str


class UserRole(TypedDict):
    id: int
    name: str


class RoleProduct(TypedDict):
    name: str


class Role(TypedDict):
    id: int
    is_admin: bool
    name: str
    products: List[RoleProduct]
    role_type: int


class ListRolesData(TypedDict):
    items: List[Role]
    paging: PagePagination
