from ..._types import TypedDict


class CurrentPagePagination(TypedDict):
    current_page: int
    pages: int
    per_page: int
    total: int


class PagePagination(TypedDict):
    page: int
    pages: int
    per_page: int
    total: int


class RowsPagination(TypedDict):
    page: int
    size: int
    total_page: int
    total_rows: int
