from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import TYPE_CHECKING, TypeAlias

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from .sponsored_product import SponsoredProduct


class AdType(Enum):
    """
    Valid Display Ad Types
    """

    BANNER = "banner"
    PRODUCT = "product"


AdUnit: TypeAlias = str


class SponsoredDisplayCreative(Enum):
    """
    Creatives as sent to and from frontends, not third-parties.

    These are mapped to third-party creatives/ad-format identifiers and are mostly the
    same, but we just use lower case on this side.

    These are either hardcoded in frontends (search-banner, single-product, pdp-banner)
    or sent with CMS Page Widgets and thus identifiers in CMS BFF must match these.
    """

    UNKNOWN = "unknown-creative"
    SINGLE_PRODUCT = "single-product"
    MULTI_PRODUCT = "multi-product"
    SEARCH_BANNER = "search-banner"
    PDP_BANNER = "pdp-banner"
    CMS_CAROUSEL = "cms-carousel"
    RIGHT_HAND_BANNER = "right-hand-banner"

    @classmethod
    def _missing_(cls, value: object) -> SponsoredDisplayCreative:
        return SponsoredDisplayCreative.UNKNOWN


@dataclass
class SponsoredDisplay:
    """Sponsored Display Ad model"""

    ad_type: AdType
    client_id: str
    ad_unit: AdUnit
    creative: SponsoredDisplayCreative
    uclid: str
    destination_url: str
    background: BannerBackgroundImages
    products: list[SponsoredProduct] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "ad_type": self.ad_type.value,
            "client_id": self.client_id,
            "ad_unit": self.ad_unit,
            "creative": self.creative.value,
            "uclid": self.uclid,
            "destination_url": self.destination_url,
            "products": [p.to_dict() for p in self.products],
            "background": {k.value: v for k, v in self.background.items()},
        }


class Breakpoint(StrEnum):
    # **Note** the order here is important, *DO NOT CHANGE THESE*

    SMALL = "sm"
    MEDIUM = "md"
    LARGE = "lg"


class BannerImage(TypedDict):
    src: str
    width: int
    height: int


BannerBackgroundImages: TypeAlias = dict[Breakpoint, BannerImage]
