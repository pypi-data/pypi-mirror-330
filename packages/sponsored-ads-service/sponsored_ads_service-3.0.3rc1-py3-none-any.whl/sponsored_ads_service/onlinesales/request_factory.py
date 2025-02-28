from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

from storefront_product_adapter.facades import HierarchyFacade
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.hierarchies import HierarchyType

from sponsored_ads_service.errors import UnsupportedLocationError
from sponsored_ads_service.factories.tools.filter import get_brands, get_keywords
from sponsored_ads_service.onlinesales.models import (
    FilterKey,
)
from sponsored_ads_service.sponsored_ads.models import Location

from .models import Device, DisplayAdPageType, DisplayRequest, ProductsRequest, SearchPageType

if TYPE_CHECKING:
    from storefront_product_adapter.adapters import ProductlineAdapter
    from tal_stats_client import StatsClient

    from sponsored_ads_service.factories.hierarchy import HierarchyFactory
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )
    from sponsored_ads_service.onlinesales.models import FilterPairs
    from sponsored_ads_service.sponsored_ads.models import (
        DisplayAdsRequest,
        ProductAdsRequest,
        Targeting,
    )

    from .creatives import CreativeFactory

logger = logging.getLogger(__name__)


class RequestFactory:
    """
    Factory class that should be used to build requests to the OnlineSales API display
    endpoint.
    """

    def __init__(
        self,
        *,
        client_id: str,
        ad_slot_id: str,
        hierarchy_factory: HierarchyFactory,
        catalogue_integration: CatalogueAggregatorIntegration,
        onlinesales_creative_factory: CreativeFactory,
        stats_client: StatsClient,
    ) -> None:
        self._client_id = client_id
        self._ad_slot_id = ad_slot_id
        self._hierarchy_factory = hierarchy_factory
        self._catalogue_integration = catalogue_integration
        self._onlinesales_creative_factory = onlinesales_creative_factory
        self._stats_client = stats_client

    def build_sponsored_display_request(self, request: DisplayAdsRequest) -> DisplayRequest:
        """
        Build and return a DisplayRequest request model, for the given
        `DisplayAdsRequest` model
        """

        filters = {}
        filters.update(self._get_filters_from_targeting(request.targeting))
        filters.update(self._get_filters_from_plids(request.targeting.plids))

        return DisplayRequest(
            client_id=self._client_id,
            device_id=request.uuid,
            page_type=DisplayAdPageType.from_location(request.location),
            device=Device.from_platform(request.platform),
            ad_units=request.ad_units,
            filters=filters,
            creatives=self._onlinesales_creative_factory.from_request_creatives(
                request.creatives, location=request.location
            ),
            preview_campaign_id=request.preview_campaign_id,
        )

    def build_products_request(self, request: ProductAdsRequest) -> ProductsRequest:
        targeting = request.targeting

        keywords = get_keywords(filters=targeting.filters, qsearch=targeting.qsearch)
        os_categories = self._hierarchy_factory.build_node_path(filters=targeting.filters)
        min_price, max_price = self._get_prices(filters=targeting.filters)
        brands = get_brands(filters=targeting.filters)
        promotion_ids_str = self.get_promotion_ids_str(targeting.filters)
        sku_ids = self._catalogue_integration.get_offer_ids_for_plids(targeting.plids or [])

        return ProductsRequest(
            cli_ubid=request.uuid,
            device=Device.from_platform(request.platform),
            sku_ids=sku_ids or [],
            pcnt=request.limit,
            page_type=self._get_products_page_type(request.location, keywords, os_categories),
            client_id=self._client_id,
            a_slot=self._ad_slot_id,
            keywords=keywords,
            page_name="DEALS" if promotion_ids_str else None,
            min_price=min_price,
            max_price=max_price,
            brands=brands,
            categories=os_categories,
            rtl_custom_label_0=promotion_ids_str,
        )

    def _get_products_page_type(
        self,
        location: Location,
        keywords: list[str] | None = None,
        categories: list[str] | None = None,
    ) -> SearchPageType:
        match location:
            case Location.SEARCH:
                if keywords:
                    return SearchPageType.SEARCH
                if categories:
                    return SearchPageType.CATEGORY
                return SearchPageType.HOME
            case Location.PDP:
                return SearchPageType.PRODUCT
            case Location.DEALS:
                return SearchPageType.CUSTOM
            case _:
                raise UnsupportedLocationError(f"Unsupported location {location}")

    def _get_filters_from_targeting(self, targeting: Targeting) -> FilterPairs:
        """
        Create and return a Dict containing OnlineSales request filter key-value pairs.

        The filters have the format `f.<key> = value`.
        """
        filter_pairs: FilterPairs = {}

        hierarchies = self._hierarchy_factory.build_node_path(filters=targeting.filters)
        if hierarchies:
            filter_pairs[FilterKey.CATEGORIES] = hierarchies

        brands = get_brands(filters=targeting.filters)
        if brands:
            filter_pairs[FilterKey.BRAND] = ",".join(brands)

        keywords = get_keywords(filters=targeting.filters, qsearch=targeting.qsearch)
        if keywords:
            filter_pairs[FilterKey.KEYWORD] = "+".join(keywords)

        return filter_pairs

    def _get_filters_from_plids(self, plids: list[int]) -> FilterPairs:
        # Onlinesales' API cannot handle multiple SKU's, brands, or categories.
        # Rather than selecting the first plid of several, we disregard
        # them entirely if there are more than one, and use the first plid
        # if there is one and only one.
        if not plids or len(plids) > 1:
            return {}
        plid = plids[0]

        catalogue_result = self._catalogue_integration.get_filtered_productline_adapters(
            plids=[plid]
        )
        productline = catalogue_result.get(str(plid))
        if not productline:
            return {}

        if productline.get_attribute_raw_value("do_not_promote_other_items_with_item"):
            # Drop the ad request if the given PLID should not have other items promoted
            # alongside it
            message = f"PLID {plid} has attribute 'do_not_promote_other_items_with_item"
            logger.debug(message)
            self._stats_client.incr(
                "custom.sponsored_display.request.filtered.do_not_promote_other"
            )
            return {}

        offer_ids = self._get_offer_ids_from_productline(productline)
        if not offer_ids:
            # Drop the ad request if no SKU filter is found for targeting
            self._stats_client.incr("custom.sponsored_display.request.filtered.no_buyable_offers")
            return {}

        return {
            FilterKey.SKU: offer_ids[0],
            FilterKey.BRAND: productline.brand_name,
            FilterKey.CATEGORIES: self._get_hierarchy_path_from_productline(productline),
        }

    @staticmethod
    def _get_prices(filters: dict[str, list[str]]) -> tuple[int | None, int | None]:
        """
        Determine the min and max prices (in the form of a `min_price`,
        `max_price` tuple) based on the existence of a `Price` filter on the
        given `request`
        """
        min_price, max_price = None, None
        price_filters = filters.get("Price")
        if price_filters and len(price_filters) == 1:
            match = re.match(r"^(\d+|\*)-(\d+|\*)$", price_filters[0].replace(" ", ""))
            if match:
                min_pg, max_pg = match.group(1), match.group(2)
                min_price = int(min_pg) if min_pg != "*" else None
                max_price = int(max_pg) if max_pg != "*" else None
        return min_price, max_price

    @staticmethod
    def get_promotion_ids_str(filters: dict[str, list[str]]) -> list[str]:
        return filters.get("Promotions") or []

    @staticmethod
    def _get_offer_ids_from_productline(productline: ProductlineAdapter) -> list[int]:
        """
        Return a list of Offer IDs for the given Productline Adapter
        """

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

    @staticmethod
    def _get_hierarchy_path_from_productline(productline: ProductlineAdapter) -> list[str]:
        """
        Return the primary path from the given Productline Adapter's lineage
        """

        merchandising_hierarchy = HierarchyFacade(
            hierarchy_type=HierarchyType.MERCHANDISING,
            productline=productline,
        )

        primary_path = merchandising_hierarchy.get_primary_path()

        return [primary_path.forest.name] + [n.name for n in primary_path.nodes]
