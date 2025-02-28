from __future__ import annotations

import os
import random
from dataclasses import dataclass
from pathlib import Path

import pkg_resources
from tal_service_config import FORMAT_LIST_OF_TUPLE, ServiceConfig

from sponsored_ads_service.errors import ConfigurationError
from sponsored_ads_service.models.validation import SponsoredProductsValidationConfig
from sponsored_ads_service.utils.singleton import SingletonMeta


@dataclass
class CircuitBreakerConfig:
    enabled: bool
    reset_timeout_s: int
    max_fail: int


@dataclass
class LocalcacheContext:
    enabled: bool
    ttl: int
    maxsize: int

    @classmethod
    def from_tal_service_config(cls, config: ServiceConfig, context: str) -> LocalcacheContext:
        enabled = config.get_bool(f"localcache.{context}_enabled", default=True)
        if enabled:
            ttl = config.get_int(f"localcache.{context}_ttl", default=None)
            if ttl is None:
                raise ConfigurationError(f"No config for: localcache.{context}_ttl")

            maxsize = config.get_int(f"localcache.{context}_maxsize", default=None)
            if maxsize is None:
                raise ConfigurationError(f"No config for: localcache.{context}_maxsize")
        else:
            ttl = 0
            maxsize = 0

        return LocalcacheContext(enabled=enabled, ttl=ttl, maxsize=maxsize)


@dataclass
class MemcacheContext:
    enabled: bool
    ttl: int

    @classmethod
    def from_tal_service_config(cls, config: ServiceConfig, context: str) -> MemcacheContext:
        enabled = config.get_bool(f"memcache.{context}_enabled", default=True)

        if enabled:
            ttl = config.get_int(f"memcache.{context}_ttl", default=None)
            if ttl is None:
                raise ConfigurationError(f"No config for: memcache.{context}_ttl")
        else:
            ttl = 0

        return MemcacheContext(enabled=enabled, ttl=ttl)


class SponsoredAdsConfig(metaclass=SingletonMeta):
    config: ServiceConfig

    def __init__(self) -> None:
        super().__init__()
        self._load_configuration()

    def _load_configuration(self) -> ServiceConfig:
        if not getattr(self, "config", None):
            role = os.environ.get("ROLE", "kubernetes").lower()
            environment = os.environ.get("ENVIRONMENT", "staging").lower()
            data_dir = Path(__file__).resolve().parent / "data"
            ini_files = [
                str((data_dir / role).with_suffix(".ini")),
                str((data_dir / environment).with_suffix(".ini")),
            ]
            self.config = ServiceConfig(ini_files=ini_files)
        return self.config

    def service_lookup(self, service_name: str) -> list[str]:
        return self.config.find_service(service_name)

    def get_version(self) -> str:
        return pkg_resources.get_distribution("sponsored_ads_service").version

    def get_statsd_settings(self) -> dict[str, str | bool]:
        endpoints = self.config.find_service("statsd", protocol="udp", format=FORMAT_LIST_OF_TUPLE)
        host, port = random.choice(endpoints)
        return {
            "service_name_prefix": "sponsored-ads-service",
            "host": host,
            "port": port,
            "include_fqdn": False,
        }

    def get_cache_settings(self) -> dict:
        nss = self.config.get_str("MEMCACHE_NAMESPACE_SUFFIX")
        return {
            "host_port": self.service_lookup("mcrouter"),
            "namespace": f"sponsored-ads-service-{nss}",
            "socket_timeout": self.config.get_int("MEMCACHE_SOCKET_TIMEOUT") or 3,
        }

    def get_sentry_settings(self) -> dict | None:
        if self.config.get_bool("SENTRY_ENABLED"):
            return {
                "release": self.get_version(),
                "environment": os.getenv("ENVIRONMENT", "staging").lower(),
                "dsn": self.config.get_str("SENTRY_DSN"),
            }
        return None

    def get_cms_nav_timeout(self) -> int:
        return self.config.get_int("TIMEOUT_CMS_NAV") or 1000

    def get_cat_legacy_service_timeout(self) -> int:
        return self.config.get_int("TIMEOUT_CAT_LEGACY_SERVICE") or 1000

    def get_cat_aggregator_service_timeout(self) -> int:
        return self.config.get_int("TIMEOUT_CAT_AGGREGATOR") or 2000

    def get_cat_api_service_timeout(self) -> int:
        return self.config.get_int("TIMEOUT_CAT_API") or 2000

    def get_online_sales_timeout(self) -> int:
        return self.config.get_int("TIMEOUT_ONLINE_SALES") or 1000

    def get_sponsored_products_client_id(self) -> str:
        return self.config.get_str("SPONSORED_PRODUCTS_CLIENT_ID")

    def get_onlinesales_ad_slot_id(self) -> str:
        return self.config.get_str("SPONSORED_PRODUCTS_AD_SLOT_ID")

    def get_sponsored_products_plid_limit(self) -> int:
        return self.config.get_int("SPONSORED_PRODUCTS_PLID_LIMIT") or 5

    def get_localcache_enabled(self) -> bool:
        return self.config.get_bool("LOCALCACHE_ENABLED")

    def get_cat_aggregator_circuitbreaker_enabled(self) -> bool:
        return self.config.get_bool("CB_CAT_AGGREGATOR_ENABLED")

    def get_cat_api_circuitbreaker_enabled(self) -> bool:
        return self.config.get_bool("CB_CAT_API_ENABLED")

    def get_onlinesales_circuitbreaker_enabled(self) -> bool:
        return self.config.get_bool("CB_ONLINESALES_ENABLED")

    def get_onlinesales_circuitbreaker_reset_timeout_default(self) -> int:
        return self.config.get_int("CB_ONLINESALES_RESET_TIMEOUT_DEFAULT")

    def get_onlinesales_circuitbreaker_reset_timeout_homepage(self) -> int:
        return self.config.get_int("CB_ONLINESALES_RESET_TIMEOUT_HOMEPAGE")

    def get_sponsored_products_validation_config(
        self,
    ) -> SponsoredProductsValidationConfig:
        """Get which validation steps are enabled for validating sponsored products"""
        return SponsoredProductsValidationConfig(
            validate_active_and_available=self.config.get_bool(
                "SPONSORED_PRODUCTS_VALIDATE_ACTIVE_AND_AVAILABLE"
            ),
            validate_attribute=self.config.get_bool("SPONSORED_PRODUCTS_VALIDATE_ATTRIBUTE"),
            validate_buybox=self.config.get_bool("SPONSORED_PRODUCTS_VALIDATE_BUYBOX"),
            validate_stock=self.config.get_bool("SPONSORED_PRODUCTS_VALIDATE_STOCK"),
            validate_images=self.config.get_bool("SPONSORED_PRODUCTS_VALIDATE_IMAGES"),
            validate_promo_price=self.config.get_bool("SPONSORED_PRODUCTS_VALIDATE_PROMO_PRICE"),
            validate_promo_quantity=self.config.get_bool(
                "SPONSORED_PRODUCTS_VALIDATE_PROMO_QUANTITY"
            ),
        )

    def get_widget_product_title(self) -> str:
        return self.config.get_str("PRODUCT_WIDGET_TITLE")

    def get_widget_deals_title(self) -> str:
        return self.config.get_str("DEALS_WIDGET_TITLE")

    def get_sponsored_products_deals_backfill_count(self) -> int:
        return self.config.get_int("SPONSORED_PRODUCTS_DEALS_BACKFILL_COUNT") or 6

    def get_sponsored_products_deals_serve_count(self) -> int:
        return self.config.get_int("SPONSORED_PRODUCTS_DEALS_SERVE_COUNT") or 12

    def get_sponsored_products_deals_products_per_widget(self) -> int:
        return self.config.get_int("SPONSORED_PRODUCTS_DEALS_PRODUCTS_PER_WIDGET") or 6

    def get_sponsored_display_client_id(self) -> str:
        return self.config.get_str("SPONSORED_DISPLAY_CLIENT_ID")

    def get_sponsored_display_search_filters_plid_limit(self) -> int:
        return self.config.get_int("SPONSORED_DISPLAY_SEARCH_FILTERS_PLID_LIMIT")

    def get_link_data_hostname(self) -> str:
        return self.config.get_str("LINK_DATA_HOSTNAME")

    def get_localcache_context(self, context: str) -> LocalcacheContext:
        return LocalcacheContext.from_tal_service_config(config=self.config, context=context)

    def get_memcache_context(self, context: str) -> MemcacheContext:
        return MemcacheContext.from_tal_service_config(config=self.config, context=context)

    def get_rollout_flag_search_banner_remap(self) -> bool:
        """
        If true, the service must remap requests for creative `search-banner` to a new
        creative ID and process the response accordingly. The response will have
        different images dimensions and field names.
        """
        return self.config.get_bool("ROLLOUT_FLAG_SEARCH_BANNER_REMAP")

    def get_circuitbreaker_config(self, service: str) -> CircuitBreakerConfig:
        return CircuitBreakerConfig(
            enabled=self.config.get_bool(f"{service}.cb_enabled"),
            reset_timeout_s=self.config.get_int(f"{service}.cb_reset_timeout_s"),
            max_fail=self.config.get_int(f"{service}.cb_max_fail"),
        )

    def get_catalogue_aggregator_cache_context(self) -> MemcacheContext:
        return MemcacheContext.from_tal_service_config(
            config=self.config, context="catalogue_aggregator"
        )

    def get_category_by_id_cache_context(self) -> MemcacheContext:
        return MemcacheContext.from_tal_service_config(
            config=self.config, context="category_by_id"
        )

    def get_departments_cache_context(self) -> MemcacheContext:
        return MemcacheContext.from_tal_service_config(config=self.config, context="departments")
