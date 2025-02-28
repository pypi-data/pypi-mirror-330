from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from storefront_product_adapter.models.catalogue_schema import ProductlineLineage

    from sponsored_ads_service.constants import NoticeKeys


@dataclass
class AdInfo:
    text_notices: list[NoticeKeys]
    image_notices: list[NoticeKeys]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OnlineSalesAdInfo(AdInfo):
    uclid: str
    client_id: str
    cli_ubid: str
    seller_id: str


@dataclass
class SponsoredProduct:
    """A singular sponsored product"""

    lineage_document: ProductlineLineage
    sponsored_ad: AdInfo

    def to_dict(self) -> dict:
        return {
            "lineage_document": self.lineage_document,
            "sponsored_ad": self.sponsored_ad.to_dict(),
        }


SponsoredProductResults = list[SponsoredProduct]


@dataclass
class WidgetTitle:
    text: str
    text_notices: list[NoticeKeys] = field(default_factory=list)


@dataclass
class DealsWidget:
    position: int
    results: SponsoredProductResults
    title: WidgetTitle


@dataclass
class ActivePromotion:
    promotion_id: int
    price: int
    qty: int
