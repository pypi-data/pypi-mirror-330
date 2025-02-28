from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import requests.exceptions
from catalogue_aggregator_client.types import FiltersV2, ItemType
from opentelemetry import trace
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus

from sponsored_ads_service.utils.circuitbreaker import ContextBreakerSet

if TYPE_CHECKING:
    from catalogue_aggregator_client.http_client import CatalogueAggregatorHttpClient
    from storefront_product_adapter.adapters import ProductlineAdapter
    from tal_stats_client import StatsClient

    from sponsored_ads_service.configuration import SponsoredAdsConfig
    from sponsored_ads_service.configuration.sponsored_ads_config import MemcacheContext
    from sponsored_ads_service.utils.memcache import Memcache


logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class CatalogueAggregatorIntegration:
    def __init__(
        self,
        aggregator_client: CatalogueAggregatorHttpClient,
        config: SponsoredAdsConfig,
        stats_client: StatsClient,
        memcache: Memcache,
    ) -> None:
        self._aggregator_client = aggregator_client
        self._config = config
        self._stats_client = stats_client
        self._logger = logging.getLogger(__name__)
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
        self._memcache = memcache

    def get_relative_url_for_plid(self, plid: int) -> str | None:
        filters = {
            "productline": {"properties": ["id", "relative_url"]},
        }
        response = self._get_productline_adapters(
            plids=[plid],
            filters=filters,
            cache_context_key=self.get_relative_url_for_plid.__name__,
        )

        if response:
            # We can safely assume that if the response is not empty, the key is in the response
            # But mypy doesn't see it that way.
            adapter = response.get(str(plid))
            if adapter:
                return adapter.relative_url
        return None

    def get_offer_ids_for_plids(self, plids: list[int]) -> list[int]:
        filters = {
            "productline": {"properties": ["id", "attributes"]},
            "variants": {
                "variant": {"properties": ["id", "availability"]},
                "offers": {"properties": ["id", "availability"]},
            },
        }
        response = self._get_productline_adapters(
            plids=plids, filters=filters, cache_context_key=self.get_offer_ids_for_plids.__name__
        )
        offer_ids_lists = [
            self._get_buyable_offers_from_productline(doc) for doc in response.values()
        ]
        return [o_id for offer_ids in offer_ids_lists for o_id in offer_ids]

    def get_filtered_productline_adapters(self, plids: list[int]) -> dict[str, ProductlineAdapter]:
        """
        Return a filtered `ProductlineAdapter`
        """
        filters = {
            "productline": {
                "properties": [
                    "id",
                    "hierarchies",
                    "attributes",
                ],
            },
            "variants": {
                "variant": {"properties": ["id", "availability"]},
                "offers": {"properties": ["id", "availability"]},
            },
        }

        return self._get_productline_adapters(
            plids=plids,
            filters=filters,
            cache_context_key=self.get_filtered_productline_adapters.__name__,
        )

    def _get_productline_adapters(
        self, plids: list[int], filters: FiltersV2, cache_context_key: str
    ) -> dict[str, ProductlineAdapter]:
        """
        Retrieve a lineage doc from catalogue (for the given `plid` and `filters`),
        create and return a `ProductlineAdapter` object from this returned document.
        """
        cache_context = self._config.get_catalogue_aggregator_cache_context()
        if cache_context.enabled:
            return self._get_productline_adapters_cached(
                cache_context, cache_context_key, plids, filters
            )
        return self._get_productline_adapters_uncached(plids, filters)

    def _get_productline_adapters_cached(
        self,
        cache_context: MemcacheContext,
        cache_context_key: str,
        plids: list[int],
        filters: FiltersV2,
    ) -> dict[str, ProductlineAdapter]:
        """
        Retrieve a lineage doc from catalogue (for the given `plid` and `filters`),
        create and return a `ProductlineAdapter` object from this returned document.

        The filters are expected to be semi-constant, so we only need to use the cache_context_key
        for context, and the plids for the cache keys.
        """

        results: dict[str, ProductlineAdapter] = self._memcache.get_multi(
            context=cache_context_key, keys=[str(r) for r in plids]
        )
        misses = [p for p in plids if str(p) not in results]
        if misses:
            response = self._get_productline_adapters_uncached(
                misses,
                filters=filters,
            )
            if response:
                self._memcache.set_multi(
                    context=cache_context_key,
                    data={str(k): v for k, v in response.items()},
                    ttl=cache_context.ttl,
                )
                results.update(response)

        return results

    @tracer.start_as_current_span("CatalogueAggregator.fetch_productline_lineage_by_type_and_ids")
    def _get_productline_adapters_uncached(
        self, plids: list[int], filters: FiltersV2
    ) -> dict[str, ProductlineAdapter]:
        """
        Retrieve a lineage doc from catalogue (for the given `plid` and `filters`),
        create and return a `ProductlineAdapter` object from this returned document.
        """
        with self._breaker_set.context("fetch_productline_lineage_by_type_and_ids"):
            response = self._aggregator_client.fetch_productline_lineage_by_type_and_ids(
                plids,
                item_type=ItemType.PRODUCTLINE,
                filters=filters,
            )
            return {
                key: AdaptersFactory.from_productline_lineage(value)
                for key, value in response.items()
            }

    @staticmethod
    def _get_buyable_offers_from_productline(productline: ProductlineAdapter) -> list[int]:
        if productline.get_attribute_raw_value("do_not_promote_other_items_with_item"):
            logger.debug(
                "PLID%d has attribute 'do_not_promote_other_items_with_item'",
                productline.productline_id,
            )
            return []

        variants = CollectionsFactory.variants_from_productline_adapter(productline)
        variants = variants.filter_by_availability([AvailabilityStatus.BUYABLE])
        offer_ids: list[int] = []
        for variant in variants:
            offers = CollectionsFactory.offers_from_variant_adapter(
                variant
            ).filter_by_availability([AvailabilityStatus.BUYABLE])
            offer_ids.extend(filter(None, (o.offer_id for o in offers)))

        logger.debug("Offer IDs %s found for PLID%d", offer_ids, productline.productline_id)
        return offer_ids
