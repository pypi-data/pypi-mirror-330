from sponsored_ads_service.configuration import Clients, SponsoredAdsConfig
from sponsored_ads_service.factories.hierarchy import HierarchyFactory
from sponsored_ads_service.integrations.catalogue_aggregator import CatalogueAggregatorIntegration
from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration
from sponsored_ads_service.integrations.route import RouteIntegration
from sponsored_ads_service.onlinesales import (
    CreativeFactory,
    DisplayClient,
    OnlinesalesFacade,
    ProductsClient,
    RequestFactory,
    ResponseFactory,
)
from sponsored_ads_service.onlinesales.destination_url_factory import DestinationUrlFactory
from sponsored_ads_service.sponsored_ads import models as dto
from sponsored_ads_service.utils.memcache import Memcache
from sponsored_ads_service.validators.link_validator import LinkValidator


class SponsoredAdsController:
    """
    Controller class for the retrieval of Sponsored Ads.
    """

    _config: SponsoredAdsConfig
    _onlinesales_facade: OnlinesalesFacade
    _request_factory: RequestFactory

    def __init__(self) -> None:
        clients = Clients()
        self._config = SponsoredAdsConfig()

        catalogue_integration = CatalogueAggregatorIntegration(
            aggregator_client=clients.cat_aggregator_client,
            config=self._config,
            stats_client=clients.stats_client,
            memcache=Memcache(
                cache_client=clients.cache_client,
                stats_client=clients.stats_client,
                service_version=self._config.get_version(),
            ),
        )

        self._onlinesales_facade = OnlinesalesFacade(
            config=self._config,
            stats_client=clients.stats_client,
            display_client=DisplayClient(
                config=self._config,
            ),
            products_client=ProductsClient(
                config=self._config,
            ),
            response_factory=ResponseFactory(
                config=self._config,
                destination_url_factory=DestinationUrlFactory(
                    config=self._config,
                    catalogue_integration=catalogue_integration,
                    link_validator=LinkValidator(
                        stats_client=clients.stats_client,
                        route_integration=RouteIntegration(cms_nav_client=clients.cms_nav_client),
                    ),
                ),
            ),
        )

        self._request_factory = RequestFactory(
            client_id=self._config.get_sponsored_display_client_id(),
            ad_slot_id=self._config.get_onlinesales_ad_slot_id(),
            hierarchy_factory=HierarchyFactory(
                hierarchy_integration=HierarchyIntegration(
                    cms_nav_client=clients.cms_nav_client,
                    cat_legacy_client=clients.cat_legacy_client,
                    memcache=Memcache(
                        cache_client=clients.cache_client,
                        stats_client=clients.stats_client,
                        service_version=self._config.get_version(),
                    ),
                    config=self._config,
                ),
            ),
            catalogue_integration=catalogue_integration,
            onlinesales_creative_factory=CreativeFactory(config=self._config),
            stats_client=clients.stats_client,
        )

    def get_sponsored_display(self, request: dto.DisplayAdsRequest) -> dto.DisplayAdsResponse:
        os_request = self._request_factory.build_sponsored_display_request(request=request)
        return self._onlinesales_facade.get_sponsored_display(request=os_request)

    def get_sponsored_products(self, request: dto.ProductAdsRequest) -> dto.ProductAdsResponse:
        os_request = self._request_factory.build_products_request(request)
        return self._onlinesales_facade.get_sponsored_products(request=os_request)
