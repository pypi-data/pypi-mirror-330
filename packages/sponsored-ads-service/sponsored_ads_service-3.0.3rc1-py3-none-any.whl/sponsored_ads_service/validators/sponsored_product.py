from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from opentelemetry import trace
from storefront_api_views_product.facades import BuyboxPreferenceFacade
from storefront_product_adapter.facades import PromotionsFacade, SummaryFacade
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.condition import OfferCondition

from sponsored_ads_service.errors import SponsoredProductValidationError

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

if TYPE_CHECKING:
    from storefront_product_adapter.adapters import (
        OfferAdapter,
        ProductlineAdapter,
        VariantAdapter,
    )
    from storefront_product_adapter.collections import VariantCollection
    from storefront_product_adapter.models.promotion import Promotion
    from tal_stats_client import StatsClient

    from sponsored_ads_service.models.validation import SponsoredProductsValidationConfig

_STATS_PREFIX = "custom.validation.sponsored_products.errors"


class _PromotionsValidator:
    def __init__(self, stats_client: StatsClient) -> None:
        self._stats_client = stats_client

    def validate(self, variants: VariantCollection, promotion_ids: list[int]) -> None:
        # A little inefficient to get all the promos then filter.
        # But no option in the lib to filter by ids currently
        active_promotions = [
            p for p in variants.get_active_promotions() if p.promotion_id in promotion_ids
        ]
        self._validate_promo_ids(active_promotions, promotion_ids)
        winning_promotion = PromotionsFacade.pick_winner_from_list(active_promotions)
        self._validate_promo_price(winning_promotion)
        self._validate_promo_quantity(winning_promotion)

    def _validate_promo_ids(
        self, active_promotions: list[Promotion], expected_promo_ids: list[int]
    ) -> None:
        active_promotion_ids = {p.promotion_id for p in active_promotions}
        if not set(expected_promo_ids).intersection(active_promotion_ids):
            self._raise_error("promotion_id", message="No requested promotion ID is active")

    def _validate_promo_price(self, promotion: Promotion | None) -> None:
        if promotion and not promotion.price:
            self._raise_error("promotion_price", message="Promotion price is not > 0")

    def _validate_promo_quantity(self, promotion: Promotion | None) -> None:
        if promotion and not promotion.quantity:
            self._raise_error("promotion_price", message="Promotion qty is not > 0")

    def _raise_error(self, error_type: str, message: str) -> None:
        self._stats_client.incr(f"{_STATS_PREFIX}.{error_type}")
        raise SponsoredProductValidationError(message, error_type=error_type)


class SponsoredProductValidator:
    def __init__(
        self,
        stats_client: StatsClient,
        validation_config: SponsoredProductsValidationConfig,
    ) -> None:
        self._stats_client = stats_client
        self._config = validation_config
        self._promotions_validator = _PromotionsValidator(stats_client=stats_client)

    @tracer.start_as_current_span("SponsoredProductValidator.validate")
    def validate(
        self,
        productline: ProductlineAdapter,
        offer_id: int,
        promotion_ids: list[int] | None = None,
        offer_opt: bool = False,
    ) -> None:
        """
        Validate that the given `productline` is considered valid for
        display as a sponsored product.
        """
        buybox_type = BuyboxType.CUSTOM_1
        if offer_opt:
            buybox_type = BuyboxPreferenceFacade.get_default_for_productline(
                productline=productline
            )

        # TODO: Do we move the variants / offer out of here
        variants = CollectionsFactory.variants_from_productline_adapter(productline)
        variants = variants.filter_by_availability([AvailabilityStatus.BUYABLE])
        winning_offer = SummaryFacade.find_overall_offer_winner(
            variants=variants,
            buybox_type=buybox_type,
            buybox_conditions_precedence=(OfferCondition.NEW,),
        )
        selected_variant = winning_offer.variant if winning_offer else None

        # Check for out of stock first. If it's out of stock it won't have a winning
        # offer anyway. The next check for has_winning_offer will then count single
        # variants where something is very wrong.
        self._validate_buyable(productline)
        self._validate_stock(winning_offer)
        self._validate_has_winning_offer(variants, winning_offer)
        if self._config.validate_buybox:
            self._validate_buybox_winner(variants, winning_offer, offer_id)
        self._validate_do_not_sponsor_attribute(productline)
        self._validate_is_not_sellable_attribute(selected_variant)
        self._validate_has_images(productline)
        if promotion_ids:
            self._promotions_validator.validate(variants, promotion_ids)

    def _validate_has_winning_offer(
        self, variants: VariantCollection, winning_offer: OfferAdapter | None
    ) -> None:
        if len(variants) > 1:
            return  # Do not check for a winning offer for variant products
        if not winning_offer:
            self._raise_error("no_winning_offer", message="Productline has no winning offer")

    def _validate_buybox_winner(
        self,
        variants: VariantCollection,
        winning_offer: OfferAdapter | None,
        offer_id: int,
    ) -> None:
        if len(variants) > 1:
            return  # Do not check buybox winner for variant products
        if winning_offer and winning_offer.offer_id != offer_id:
            self._raise_error(
                "buybox",
                message=(
                    f"Provided Offer ID {offer_id} is not the buybox "
                    f"winner ({winning_offer.offer_id})"
                ),
            )

    def _validate_buyable(self, productline: ProductlineAdapter) -> None:
        if productline.availability != AvailabilityStatus.BUYABLE:
            self._raise_error("buyable", message="Productline is not buyable")

    def _validate_do_not_sponsor_attribute(self, productline: ProductlineAdapter) -> None:
        if productline.get_attribute_raw_value("do_not_sponsor"):
            self._raise_error(
                "do_not_sponsor", message="Productline is marked as `do_not_sponsor`"
            )

    def _validate_is_not_sellable_attribute(self, variant: VariantAdapter | None) -> None:
        if variant and variant.get_attribute_raw_value("is_not_sellable"):
            self._raise_error("is_not_sellable", message="Variant is marked as `is_not_sellable`")

    def _validate_stock(self, offer: OfferAdapter | None) -> None:
        if offer and not offer.get_stock_status().is_buyable():
            self._raise_error("stock", message="Offer is considered out of stock")

    def _validate_has_images(self, productline: ProductlineAdapter) -> None:
        if not productline.cover_image_key:
            self._raise_error("images", message="Productline is missing images")

    def _raise_error(self, error_type: str, message: str) -> None:
        self._stats_client.incr(f"{_STATS_PREFIX}.{error_type}")
        raise SponsoredProductValidationError(message, error_type=error_type)
