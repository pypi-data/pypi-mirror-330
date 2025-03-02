# VTEXPY
[![PyPI Version](https://img.shields.io/pypi/v/vtexpy.svg)](https://pypi.python.org/pypi/vtexpy)

## Unofficial VTEX API's Python SDK

VTEXPY is an unofficial Python SDK designed to facilitate integration with the VTEX API.

Even though it is still tagged as beta, vtexpy has been in use by a _SaaS_ company in a
production environment for over a year, making millions of requests a day to the VTEX
API. The only reason why it is tagged as beta is that it is still under heavy
development and breaking changes are expected on the external API.

### Features

- Easy to use Python interface for calling VTEX API endpoints
- Response format standardization
- Custom exception handling
- Automatic request retrying
- Request logging

### Getting Started

#### Requirements

- Python >= 3.9, < 3.14

#### Installation

```bash
pip install vtexpy
```

#### Usage

If the API you want to call is not yet implemented, feel free to create an issue on the
VTEXPY Github repository and request it to be added.

```python
from vtex import VTEX, VTEXConfig

# Instantiate your VTEX API configuration:
vtex_config = VTEXConfig(
    account_name="<ACCOUNT_NAME>",
    app_key="<APP_KEY>",
    app_token="<APP_TOKEN>",
    # Other arguments such as: retrying, logging, etc...
)

# Instantiate the VTEX client with your configuration:
vtex_client = VTEX(config=vtex_config)

# Call one of the available APIs, e.g.:
account_response = vtex_client.license_manager.get_account()
list_sku_ids_response = vtex_client.catalog.list_sku_ids(page=1, page_size=1000)
list_orders_response = vtex_client.orders.list_orders(page=1, page_size=100)

# If the API you want to call is not yet implemented you can use the `custom` API.
response = vtex_client.custom.request(
    method="GET",
    environment="vtexcommercestable",
    endpoint="/api/catalog_system/pvt/commercialcondition/list",
    # Other arguments such as: query params, headers, json data, response class, etc...
)
```
