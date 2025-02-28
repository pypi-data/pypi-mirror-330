from requests import Response
from requests.exceptions import JSONDecodeError
from rest_clients.abstract_client import AbstractClient
from rest_clients.exceptions import (
    DuplicateConstraintViolationException,
    InvalidServiceResponseException,
    ResourceNotFoundException,
    ValidationErrorException,
)
from rest_clients.typing import JSON

from sponsored_ads_service.configuration import SponsoredAdsConfig
from sponsored_ads_service.onlinesales.models import (
    DisplayRequest,
    ProductsRequest,
)


class _BaseOnlineSalesClient(AbstractClient):
    SERVICE_NAME = "onlinesales"

    _config: SponsoredAdsConfig

    def __init__(self, config: SponsoredAdsConfig, host: str) -> None:
        self._config = config
        super().__init__(
            self.SERVICE_NAME,
            service_endpoint=host,
            protocol="https",
            timeout_seconds=self._config.get_online_sales_timeout() / 1000,
        )

    def decode_response(self, response: Response) -> JSON:
        """This method is used to decode and/or parse the returned response object from requests

        Args:
            response: The response object to be parsed

        Returns:
            The json decoded response.

        Raises:
            InvalidServiceResponseException: If the response is not a
            valid JSON response of the status code is
                not recognised. Recognised status codes are 400, 404, 409.
            ValidationErrorException: If the response status code is 400,
            this error will be raised
            ResourceNotFoundException: If the response status code is 404,
             this error will be raised
            DuplicateConstraintViolationException: If the response status code is 409,
            this error will be raised
        """
        status = response.status_code
        try:
            body = response.json()
        except JSONDecodeError:
            # If valid response (200-299) this will cause InvalidServiceBlah,
            # else correct exception will propagate:)
            body = {"error": {"message": response.text}}

        if 200 <= status <= 299:
            if body is None:
                raise InvalidServiceResponseException("Response body is empty.")
            if not body.get("error"):
                return body

        # handle 400 - Client error/ validation errors
        if status == 400:
            raise ValidationErrorException(body["error"]["message"])

        # handle 404 - Resource not found
        if status == 404:
            raise ResourceNotFoundException(body["error"]["message"])

        # handle 409 - Conflicting resource
        if status == 409:
            raise DuplicateConstraintViolationException(body["error"]["message"])

        raise InvalidServiceResponseException(
            body.get("error", {}).get(
                "message", "An error occurred during communication with the api."
            ),
        )


class DisplayClient(_BaseOnlineSalesClient):
    def __init__(self, config: SponsoredAdsConfig) -> None:
        super().__init__(config, "tal-ba.o-s.io")

    def _get_url(self, request: DisplayRequest) -> str:
        if not request.preview_campaign_id:
            return "/v2/bsda"
        return "/preview/bsda"

    def get_display_ads(self, request: DisplayRequest) -> dict:
        return self.get(
            resource_path=self._get_url(request),
            params=request.to_request_params(),
            operation_name=self.get_display_ads.__name__,
        )


class ProductsClient(_BaseOnlineSalesClient):
    def __init__(self, config: SponsoredAdsConfig) -> None:
        super().__init__(config, "tal.o-s.io")

    def get_products_ads(self, request: ProductsRequest) -> dict:
        return self.get(
            resource_path="/sda",
            params=request.to_request_params(),
            operation_name=self.get_products_ads.__name__,
        )
