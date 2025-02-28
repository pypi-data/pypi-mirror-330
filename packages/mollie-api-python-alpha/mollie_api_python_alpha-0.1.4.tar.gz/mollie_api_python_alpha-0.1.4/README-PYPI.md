# mollie-api-python-alpha

Developer-friendly & type-safe Python SDK specifically catered to leverage *mollie-api-python-alpha* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=mollie-api-python-alpha&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<br /><br />
> [!IMPORTANT]
> This SDK is not yet ready for production use. To complete setup please follow the steps outlined in your [workspace](https://app.speakeasy.com/org/mollie-oom/mollie). Delete this section before > publishing to a package manager.

<!-- Start Summary [summary] -->
## Summary


<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [mollie-api-python-alpha](#mollie-api-python-alpha)
  * [SDK Installation](#sdk-installation)
  * [IDE Support](#ide-support)
  * [SDK Example Usage](#sdk-example-usage)
  * [Authentication](#authentication)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Resource Management](#resource-management)
  * [Debugging](#debugging)
* [Development](#development)
  * [Maturity](#maturity)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install mollie-api-python-alpha
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add mollie-api-python-alpha
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from mollie-api-python-alpha python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "mollie-api-python-alpha",
# ]
# ///

from mollie_api_python_alpha import Client

sdk = Client(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
import mollie_api_python_alpha
from mollie_api_python_alpha import Client
import os


with Client(
    security=mollie_api_python_alpha.Security(
        api_key=os.getenv("CLIENT_API_KEY", ""),
    ),
) as client:

    res = client.balances.list(currency="EUR", from_="bal_gVMhHKqSSRYJyPsuoPNFH")

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import mollie_api_python_alpha
from mollie_api_python_alpha import Client
import os

async def main():

    async with Client(
        security=mollie_api_python_alpha.Security(
            api_key=os.getenv("CLIENT_API_KEY", ""),
        ),
    ) as client:

        res = await client.balances.list_async(currency="EUR", from_="bal_gVMhHKqSSRYJyPsuoPNFH")

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security schemes globally:

| Name      | Type   | Scheme       | Environment Variable |
| --------- | ------ | ------------ | -------------------- |
| `api_key` | http   | HTTP Bearer  | `CLIENT_API_KEY`     |
| `o_auth`  | oauth2 | OAuth2 token | `CLIENT_O_AUTH`      |

You can set the security parameters through the `security` optional parameter when initializing the SDK client instance. The selected scheme will be used by default to authenticate with the API for all operations that support it. For example:
```python
import mollie_api_python_alpha
from mollie_api_python_alpha import Client
import os


with Client(
    security=mollie_api_python_alpha.Security(
        api_key=os.getenv("CLIENT_API_KEY", ""),
    ),
) as client:

    res = client.balances.list(currency="EUR", from_="bal_gVMhHKqSSRYJyPsuoPNFH")

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [balances](docs/sdks/balances/README.md)

* [list](docs/sdks/balances/README.md#list) - List balances
* [get](docs/sdks/balances/README.md#get) - Get balance
* [get_primary](docs/sdks/balances/README.md#get_primary) - Get primary balance
* [get_report](docs/sdks/balances/README.md#get_report) - Get balance report
* [list_transactions](docs/sdks/balances/README.md#list_transactions) - List balance transactions

### [capabilities](docs/sdks/capabilities/README.md)

* [list](docs/sdks/capabilities/README.md#list) - List capabilities

### [captures](docs/sdks/captures/README.md)

* [create](docs/sdks/captures/README.md#create) - Create capture
* [list](docs/sdks/captures/README.md#list) - List captures
* [get](docs/sdks/captures/README.md#get) - Get capture

### [chargebacks](docs/sdks/chargebacks/README.md)

* [list](docs/sdks/chargebacks/README.md#list) - List payment chargebacks
* [get](docs/sdks/chargebacks/README.md#get) - Get payment chargeback
* [list_all](docs/sdks/chargebacks/README.md#list_all) - List all chargebacks


### [client_links](docs/sdks/clientlinks/README.md)

* [create](docs/sdks/clientlinks/README.md#create) - Create client link

### [clients](docs/sdks/clients/README.md)

* [list](docs/sdks/clients/README.md#list) - List clients
* [get](docs/sdks/clients/README.md#get) - Get client

### [customers](docs/sdks/customers/README.md)

* [create](docs/sdks/customers/README.md#create) - Create customer
* [list](docs/sdks/customers/README.md#list) - List customers
* [get](docs/sdks/customers/README.md#get) - Get customer
* [update](docs/sdks/customers/README.md#update) - Update customer
* [delete](docs/sdks/customers/README.md#delete) - Delete customer
* [create_payment](docs/sdks/customers/README.md#create_payment) - Create customer payment
* [list_payments](docs/sdks/customers/README.md#list_payments) - List customer payments

### [delayed_routing](docs/sdks/delayedrouting/README.md)

* [create](docs/sdks/delayedrouting/README.md#create) - Create a delayed route
* [list](docs/sdks/delayedrouting/README.md#list) - List payment routes

### [invoices](docs/sdks/invoices/README.md)

* [list](docs/sdks/invoices/README.md#list) - List invoices
* [get](docs/sdks/invoices/README.md#get) - Get invoice

### [mandates](docs/sdks/mandates/README.md)

* [create](docs/sdks/mandates/README.md#create) - Create mandate
* [list](docs/sdks/mandates/README.md#list) - List mandates
* [get](docs/sdks/mandates/README.md#get) - Get mandate
* [revoke](docs/sdks/mandates/README.md#revoke) - Revoke mandate

### [methods](docs/sdks/methods/README.md)

* [list](docs/sdks/methods/README.md#list) - List payment methods
* [list_all](docs/sdks/methods/README.md#list_all) - List all payment methods
* [get](docs/sdks/methods/README.md#get) - Get payment method
* [enable_method](docs/sdks/methods/README.md#enable_method) - Enable payment method
* [disable_method](docs/sdks/methods/README.md#disable_method) - Disable payment method
* [enable_method_issuer](docs/sdks/methods/README.md#enable_method_issuer) - Enable payment method issuer
* [disable_method_issuer](docs/sdks/methods/README.md#disable_method_issuer) - Disable payment method issuer

### [onboarding](docs/sdks/onboarding/README.md)

* [get](docs/sdks/onboarding/README.md#get) - Get onboarding status
* [create](docs/sdks/onboarding/README.md#create) - Submit onboarding data

### [orders](docs/sdks/orders/README.md)

* [create](docs/sdks/orders/README.md#create) - Create order
* [list](docs/sdks/orders/README.md#list) - List orders
* [get](docs/sdks/orders/README.md#get) - Get order
* [update](docs/sdks/orders/README.md#update) - Update order
* [cancel](docs/sdks/orders/README.md#cancel) - Cancel order
* [manage_lines](docs/sdks/orders/README.md#manage_lines) - Manage order lines
* [cancel_lines](docs/sdks/orders/README.md#cancel_lines) - Cancel order lines
* [update_line](docs/sdks/orders/README.md#update_line) - Update order line
* [create_payment](docs/sdks/orders/README.md#create_payment) - Create order payment

### [organizations](docs/sdks/organizations/README.md)

* [get](docs/sdks/organizations/README.md#get) - Get organization
* [get_current](docs/sdks/organizations/README.md#get_current) - Get current organization
* [get_partner_status](docs/sdks/organizations/README.md#get_partner_status) - Get partner status

### [payment_links](docs/sdks/paymentlinks/README.md)

* [create](docs/sdks/paymentlinks/README.md#create) - Create payment link
* [list](docs/sdks/paymentlinks/README.md#list) - List payment links
* [get](docs/sdks/paymentlinks/README.md#get) - Get payment link
* [update](docs/sdks/paymentlinks/README.md#update) - Update payment link
* [delete](docs/sdks/paymentlinks/README.md#delete) - Delete payment link
* [get_payments](docs/sdks/paymentlinks/README.md#get_payments) - Get payment link payments

### [payments](docs/sdks/payments/README.md)

* [create](docs/sdks/payments/README.md#create) - Create payment
* [list](docs/sdks/payments/README.md#list) - List payments
* [get](docs/sdks/payments/README.md#get) - Get payment
* [update](docs/sdks/payments/README.md#update) - Update payment
* [cancel](docs/sdks/payments/README.md#cancel) - Cancel payment
* [release_authorization](docs/sdks/payments/README.md#release_authorization) - Release payment authorization

### [permissions](docs/sdks/permissions/README.md)

* [list](docs/sdks/permissions/README.md#list) - List permissions
* [get](docs/sdks/permissions/README.md#get) - Get permission

### [profiles](docs/sdks/profiles/README.md)

* [create](docs/sdks/profiles/README.md#create) - Create profile
* [list](docs/sdks/profiles/README.md#list) - List profiles
* [get](docs/sdks/profiles/README.md#get) - Get profile
* [update](docs/sdks/profiles/README.md#update) - Update profile
* [delete](docs/sdks/profiles/README.md#delete) - Delete profile
* [get_current](docs/sdks/profiles/README.md#get_current) - Get current profile

### [refunds](docs/sdks/refunds/README.md)

* [create](docs/sdks/refunds/README.md#create) - Create payment refund
* [list](docs/sdks/refunds/README.md#list) - List payment refunds
* [get](docs/sdks/refunds/README.md#get) - Get payment refund
* [cancel](docs/sdks/refunds/README.md#cancel) - Cancel payment refund
* [create_order](docs/sdks/refunds/README.md#create_order) - Create order refund
* [list_order](docs/sdks/refunds/README.md#list_order) - List order refunds
* [list_all](docs/sdks/refunds/README.md#list_all) - List all refunds

### [settlements](docs/sdks/settlements/README.md)

* [list](docs/sdks/settlements/README.md#list) - List settlements
* [get](docs/sdks/settlements/README.md#get) - Get settlement
* [get_open](docs/sdks/settlements/README.md#get_open) - Get open settlement
* [get_next](docs/sdks/settlements/README.md#get_next) - Get next settlement
* [get_payments](docs/sdks/settlements/README.md#get_payments) - Get settlement payments
* [get_captures](docs/sdks/settlements/README.md#get_captures) - Get settlement captures
* [get_refunds](docs/sdks/settlements/README.md#get_refunds) - Get settlement refunds
* [get_chargebacks](docs/sdks/settlements/README.md#get_chargebacks) - Get settlement chargebacks

### [shipments](docs/sdks/shipments/README.md)

* [create](docs/sdks/shipments/README.md#create) - Create shipment
* [list](docs/sdks/shipments/README.md#list) - List shipments
* [get](docs/sdks/shipments/README.md#get) - Get shipment
* [update](docs/sdks/shipments/README.md#update) - Update shipment

### [subscriptions](docs/sdks/subscriptions/README.md)

* [create](docs/sdks/subscriptions/README.md#create) - Create subscription
* [list](docs/sdks/subscriptions/README.md#list) - List customer subscriptions
* [get](docs/sdks/subscriptions/README.md#get) - Get subscription
* [update](docs/sdks/subscriptions/README.md#update) - Update subscription
* [cancel](docs/sdks/subscriptions/README.md#cancel) - Cancel subscription
* [list_all](docs/sdks/subscriptions/README.md#list_all) - List all subscriptions
* [list_payments](docs/sdks/subscriptions/README.md#list_payments) - List subscription payments

### [terminals](docs/sdks/terminals/README.md)

* [list](docs/sdks/terminals/README.md#list) - List terminals
* [get](docs/sdks/terminals/README.md#get) - Get terminal

### [wallets](docs/sdks/wallets/README.md)

* [request_apple_pay_payment_session](docs/sdks/wallets/README.md#request_apple_pay_payment_session) - Request Apple Pay payment session

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
import mollie_api_python_alpha
from mollie_api_python_alpha import Client
from mollie_api_python_alpha.utils import BackoffStrategy, RetryConfig
import os


with Client(
    security=mollie_api_python_alpha.Security(
        api_key=os.getenv("CLIENT_API_KEY", ""),
    ),
) as client:

    res = client.balances.list(currency="EUR", from_="bal_gVMhHKqSSRYJyPsuoPNFH",
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
import mollie_api_python_alpha
from mollie_api_python_alpha import Client
from mollie_api_python_alpha.utils import BackoffStrategy, RetryConfig
import os


with Client(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    security=mollie_api_python_alpha.Security(
        api_key=os.getenv("CLIENT_API_KEY", ""),
    ),
) as client:

    res = client.balances.list(currency="EUR", from_="bal_gVMhHKqSSRYJyPsuoPNFH")

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `list_async` method may raise the following exceptions:

| Error Type                                      | Status Code | Content Type         |
| ----------------------------------------------- | ----------- | -------------------- |
| models.ListBalancesBalancesResponseBody         | 400         | application/hal+json |
| models.ListBalancesBalancesResponseResponseBody | 404         | application/hal+json |
| models.APIError                                 | 4XX, 5XX    | \*/\*                |

### Example

```python
import mollie_api_python_alpha
from mollie_api_python_alpha import Client, models
import os


with Client(
    security=mollie_api_python_alpha.Security(
        api_key=os.getenv("CLIENT_API_KEY", ""),
    ),
) as client:
    res = None
    try:

        res = client.balances.list(currency="EUR", from_="bal_gVMhHKqSSRYJyPsuoPNFH")

        # Handle response
        print(res)

    except models.ListBalancesBalancesResponseBody as e:
        # handle e.data: models.ListBalancesBalancesResponseBodyData
        raise(e)
    except models.ListBalancesBalancesResponseResponseBody as e:
        # handle e.data: models.ListBalancesBalancesResponseResponseBodyData
        raise(e)
    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import mollie_api_python_alpha
from mollie_api_python_alpha import Client
import os


with Client(
    server_url="https://api.mollie.com/v2",
    security=mollie_api_python_alpha.Security(
        api_key=os.getenv("CLIENT_API_KEY", ""),
    ),
) as client:

    res = client.balances.list(currency="EUR", from_="bal_gVMhHKqSSRYJyPsuoPNFH")

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from mollie_api_python_alpha import Client
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Client(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from mollie_api_python_alpha import Client
from mollie_api_python_alpha.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Client(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Client` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
import mollie_api_python_alpha
from mollie_api_python_alpha import Client
import os
def main():

    with Client(
        security=mollie_api_python_alpha.Security(
            api_key=os.getenv("CLIENT_API_KEY", ""),
        ),
    ) as client:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Client(
        security=mollie_api_python_alpha.Security(
            api_key=os.getenv("CLIENT_API_KEY", ""),
        ),
    ) as client:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from mollie_api_python_alpha import Client
import logging

logging.basicConfig(level=logging.DEBUG)
s = Client(debug_logger=logging.getLogger("mollie_api_python_alpha"))
```

You can also enable a default debug logger by setting an environment variable `CLIENT_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=mollie-api-python-alpha&utm_campaign=python)
