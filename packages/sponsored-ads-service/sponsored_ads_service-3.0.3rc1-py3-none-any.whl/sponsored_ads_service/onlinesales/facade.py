import logging
from contextlib import nullcontext

import requests.exceptions
from rest_clients.exceptions import RestClientException
from tal_stats_client import StatsClient

from sponsored_ads_service.configuration import SponsoredAdsConfig
from sponsored_ads_service.errors import DownstreamError
from sponsored_ads_service.onlinesales.integration import DisplayClient, ProductsClient
from sponsored_ads_service.sponsored_ads.models import DisplayAdsResponse, ProductAdsResponse
from sponsored_ads_service.utils.circuitbreaker import CircuitBreaker, ContextBreakerSet

from .models import (
    Creative,
    Display,
    DisplayAdPageType,
    DisplayRequest,
    DisplayResponse,
    Product,
    ProductElement,
    ProductsRequest,
    ProductsResponse,
    ResponseDisplayObject,
    ResponseElements,
    SearchPageType,
)
from .response_factory import ResponseFactory


class OnlinesalesFacade:
    _client_id: str
    _display_client: DisplayClient
    _products_client: ProductsClient
    _config: SponsoredAdsConfig
    _stats_client: StatsClient
    _response_factory: ResponseFactory

    _stats_prefix = "custom.onlinesales"

    def __init__(
        self,
        config: SponsoredAdsConfig,
        stats_client: StatsClient,
        display_client: DisplayClient,
        products_client: ProductsClient,
        response_factory: ResponseFactory,
    ) -> None:
        self._logger = logging.getLogger(__name__)
        self._config = config
        self._stats_client = stats_client
        self._display_client = display_client
        self._products_client = products_client
        self._response_factory = response_factory
        self._breaker_reset_timeout_homepage = (
            self._config.get_onlinesales_circuitbreaker_reset_timeout_homepage()
        )
        self._breaker_reset_timeout_default = (
            self._config.get_onlinesales_circuitbreaker_reset_timeout_default()
        )
        self._breaker_set = ContextBreakerSet(
            config=self._config.get_circuitbreaker_config("onlinesales"),
            upstream="onlinesales",
            error_types=(
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ),
            logger=self._logger,
            stats_client=self._stats_client,
        )
        self._stats_key_fetch_display_ads = f"{self._stats_prefix}.fetch_display_ads"
        self._stats_key_fetch_display_ads_preview = (
            f"{self._stats_prefix}.fetch_display_ads_preview"
        )
        self._stats_key_fetch_sponsored_products = f"{self._stats_prefix}.fetch_sponsored_products"

    def get_sponsored_display(self, request: DisplayRequest) -> DisplayAdsResponse:
        if not request.preview_campaign_id:
            stats_key = f"{self._stats_key_fetch_display_ads}.{request.page_type.value.lower()}"
            request_context = self._get_onlinesales_request_context(
                page_type=request.page_type, preview_mode=False
            )
        else:
            # For ad requests initiated by internal users, use stats and a
            # circuitbreaker separate from normal public traffic, mostly because these
            # use separate URLs and if that means separate backends we don't want
            # preview requests to succeed and reset the circuitbreaker.
            stats_key = (
                f"{self._stats_key_fetch_display_ads_preview}.{request.page_type.value.lower()}"
            )
            request_context = self._get_onlinesales_request_context(
                page_type=request.page_type, preview_mode=True
            )

        try:
            self._stats_client.incr(f"{stats_key}.ad_units_requested", len(request.ad_units))

            with request_context:
                data = self._display_client.get_display_ads(request)

            self._stats_client.incr(f"{stats_key}.ad_units_returned", len(data.get("ads", [])))
        except RestClientException:
            raise DownstreamError("onlinesales")

        ads = []
        for au_ads in data.get("ads", {}).values():
            for ad_object in au_ads:
                ad = self._build_display_ad(ad_object)
                ads.append(ad)
                self._stats_client.incr(f"{stats_key}.products_returned", len(ad.products))

        return self._response_factory.build_display_ad_response(
            DisplayResponse(ads=ads), request.device_id
        )

    def get_sponsored_products(self, request: ProductsRequest) -> ProductAdsResponse:
        stats_key_suffix = request.page_type.value.lower()
        stats_key = f"{self._stats_key_fetch_sponsored_products}.{stats_key_suffix}"

        try:
            request_context = self._get_onlinesales_request_context(
                page_type=request.page_type, preview_mode=False
            )
            with request_context, self._stats_client.timer(f"{stats_key}.timing"):
                data = self._products_client.get_products_ads(request)
        except RestClientException:
            logging.exception("Error fetching sponsored ads")
            raise DownstreamError("onlinesales")

        product_elements: list[ProductElement] = []
        for p in data.get("products", []):
            if all(p.get(key) for key in ("uclid", "sku_id", "plid", "seller_id")):
                product_elements.append(p)
        product_elements = self._deduplicate_os_products(product_elements)
        # Only count both stats after a successful call. Don't want
        # retries skewing these counters.
        self._stats_client.incr(f"{stats_key}.requested", request.pcnt)
        self._stats_client.incr(f"{stats_key}.returned", len(product_elements))
        products_response = ProductsResponse(
            products=[
                Product(
                    uclid=p["uclid"],
                    sku_id=int(p["sku_id"]),
                    plid=int(p["plid"]),
                    seller_id=p["seller_id"],
                    tsin=int(p["tsin"]) if p.get("tsin") else None,
                )
                for p in product_elements
            ]
        )

        return self._response_factory.build_product_ad_response(
            products_response, request.cli_ubid
        )

    def _get_onlinesales_request_context(
        self, *, page_type: SearchPageType | DisplayAdPageType, preview_mode: bool
    ) -> CircuitBreaker | nullcontext:
        """
        Find and return an appropriate context for the request to OnlineSales.
        We need to define a circuitbreaker with a reset time based on the page type.
        """
        page_type_str = page_type.value.lower()

        if preview_mode:
            context = f"onlinesales_request_context_{page_type_str}_preview"
        else:
            context = f"onlinesales_request_context_{page_type_str}"
        breaker = self._breaker_set.context(context)

        if isinstance(breaker, nullcontext):
            return breaker

        breaker.reset_timeout = (
            self._breaker_reset_timeout_homepage
            if page_type == DisplayAdPageType.HOME
            else self._breaker_reset_timeout_default
        )

        return breaker

    def _build_display_ad(
        self,
        ad_object: ResponseDisplayObject,
    ) -> Display:
        """
        Build and return an `OnlineSalesDisplay` instance from the given API response
        object
        """

        return Display(
            ad_type=ad_object["elements"]["ad_type"],
            client_id=str(ad_object["client_id"]),
            ad_unit=ad_object["au"],
            uclid=ad_object["uclid"],
            creative=Creative(ad_object["crt"]),
            products=self._build_products_from_elements(elements=ad_object["elements"]),
            destination_url=ad_object["elements"].get("destination_url", ""),
            images={
                k: v
                for k, v in ad_object["elements"].items()
                if "_img_" in k and isinstance(v, str)
            },
        )

    def _build_products_from_elements(self, elements: ResponseElements) -> list[Product]:
        """
        Build and return a list of `Product` instances from the given API
        response object `elements`
        """

        product_elements = self._normalise_product_elements(elements)
        product_elements = self._deduplicate_os_products(product_elements)

        return [
            Product(
                uclid=product["uclid"],
                sku_id=int(product["sku_id"]),
                plid=int(product["plid"]),
                seller_id=product["seller_id"],
                tsin=int(product["tsin"]) if product.get("tsin") else None,
            )
            for product in product_elements
        ]

    def _normalise_product_elements(self, elements: ResponseElements) -> list[ProductElement]:
        """
        Build and return a list of `ProductElement` model instances from the given API
        response object `elements`. The structure of this input will vary based on the
        advert type, as `landing_product_list` items do not contain a `uclid` property
        """

        product_list = elements.get("product_list", [])
        if not product_list:
            product_list = elements.get("landing_product_list", [])

        return [
            ProductElement(
                sku_id=item["sku_id"],
                tsin=item["tsin"],
                plid=item["plid"],
                seller_id=item["seller_id"],
                uclid=item.get("uclid", ""),
            )
            for item in product_list
            if all(item.get(key) for key in ("sku_id", "plid", "seller_id"))
        ]

    def _deduplicate_os_products(self, data: list[ProductElement]) -> list[ProductElement]:
        """
        Remove online sales products with duplicate plid values.

        We need to keep the order of the products as we received it from OnlineSales.
        Duplicates that appear later in the list are removed, but the order is kept.
        """
        done = set()
        result = []
        for p in data:
            if p["plid"] not in done:
                done.add(p["plid"])
                result.append(p)
            else:
                self._stats_client.incr(f"{self._stats_prefix}.product_counts.duplicate_plid")
        return result
