import random

from cache_client.memcached import MemcachedClient
from catalogue_aggregator_client.http_client import CatalogueAggregatorHttpClient
from cms_navigation_client import CmsNavigationClient
from s4f_clients.catalogue_legacy import CatalogueLegacyServiceClient
from tal_stats_client import StatsClient

from sponsored_ads_service.utils.singleton import SingletonMeta

from .sponsored_ads_config import SponsoredAdsConfig


class Clients(metaclass=SingletonMeta):
    _config: SponsoredAdsConfig

    stats_client: StatsClient
    cache_client: MemcachedClient
    cms_nav_client: CmsNavigationClient
    cat_legacy_client: CatalogueLegacyServiceClient
    cat_aggregator_client: CatalogueAggregatorHttpClient

    def __init__(self) -> None:
        super().__init__()
        self._configure()

    def _configure(self) -> None:
        if not getattr(self, "_config", None):
            self._config = SponsoredAdsConfig()

        self._configure_statsd_client()
        self._configure_cache_client()
        self._configure_cms_nav_client()
        self._configure_catalogue_legacy_client()
        self._configure_catalogue_aggregator_client()

    def _configure_statsd_client(self) -> None:
        if not getattr(self, "stats_client", None):
            self.stats_client = StatsClient()
            stats_config = self._config.get_statsd_settings()
            self.stats_client.configure_for_service(
                service_name=stats_config["service_name_prefix"],
                stats_host=stats_config["host"],
                stats_port=stats_config["port"],
                include_fqdn=False,
            )

    def _configure_cache_client(self) -> None:
        if not getattr(self, "cache_client", None):
            self.cache_client = MemcachedClient()
            cache_config = self._config.get_cache_settings()
            self.cache_client.configure(
                hosts_and_ports=cache_config["host_port"],
                namespace=cache_config["namespace"],
                socket_timeout=cache_config["socket_timeout"],
            )

    def _configure_cms_nav_client(self) -> None:
        if not getattr(self, "cms_nav_client", None):
            self.cms_nav_client = CmsNavigationClient(
                endpoints=self._config.service_lookup("cms_navigation_service"),
                recv_timeout=self._config.get_cms_nav_timeout(),
            )

    def _configure_catalogue_legacy_client(self) -> None:
        if not getattr(self, "cat_legacy_client", None):
            self.cat_legacy_client = CatalogueLegacyServiceClient(
                endpoints=self._config.service_lookup("s4f_catalogue_legacy"),
                recv_timeout=self._config.get_cat_legacy_service_timeout(),
            )

    def _configure_catalogue_aggregator_client(self) -> None:
        if not getattr(self, "cat_aggregator_client", None):
            endpoints = self._config.service_lookup("catalogue_aggregator")
            timeout = self._config.get_cat_aggregator_service_timeout() / 1000
            self.cat_aggregator_client = CatalogueAggregatorHttpClient(
                service_endpoint=random.choice(endpoints),
                timeout_seconds=timeout,
            )
