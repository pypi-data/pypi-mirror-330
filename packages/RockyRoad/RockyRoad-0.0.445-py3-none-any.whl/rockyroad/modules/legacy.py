from .module_imports import key
from uplink.retry.when import status
from uplink import (
    Consumer,
    get as http_get,
    returns,
    headers,
    retry,
    Query,
)


@headers({"Ocp-Apim-Subscription-Key": key})
@retry(max_attempts=4, when=status(500))
class HelloWorld(Consumer):
    def __init__(self, Resource, *args, **kw):
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("")
    def list(self):
        """This call will return Hello World."""


@headers({"Ocp-Apim-Subscription-Key": key})
@retry(max_attempts=4, when=status(500))
class Dealers(Consumer):
    def __init__(self, Resource, *args, **kw):
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("dealers")
    def list(self):
        """This call will return a list of dealers."""


@headers({"Ocp-Apim-Subscription-Key": key})
@retry(max_attempts=4, when=status(500))
class Customers(Consumer):
    def __init__(self, Resource, *args, **kw):
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("customers")
    def list(self, dealer_name: Query):
        """This call will return a list of customers and machines supported by the specified dealer."""
