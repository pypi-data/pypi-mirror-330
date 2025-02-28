from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import assert_never

from sponsored_ads_service.protobuf import sponsored_ads_service_pb2 as pb


class Location(Enum):
    """
    Location of the ad
    """

    UNSPECIFIED = 0
    SEARCH = 1
    DEALS = 2
    PDP = 3
    HOME = 4
    LANDING_PAGE = 5
    ORDERS = 6
    ORDER_DETAILS = 7
    ORDER_TRACKING = 8
    ORDER_CONFIRMATION = 9
    CART = 10


class Platform(Enum):
    """
    Platform of the ad
    """

    UNSPECIFIED = 0
    WEB = 1
    ANDROID = 2
    IOS = 3


class Creative(Enum):
    """
    Creatives as sent to and from frontends.
    """

    UNSPECIFIED = 0
    BANNER = 1
    SINGLE_PRODUCT = 2
    MULTI_PRODUCT = 3

    def to_pb(self) -> pb.Creative:
        match self:
            case Creative.UNSPECIFIED:
                return pb.CREATIVE_UNSPECIFIED
            case Creative.BANNER:
                return pb.CREATIVE_BANNER
            case Creative.SINGLE_PRODUCT:
                return pb.CREATIVE_SINGLE_PRODUCT
            case Creative.MULTI_PRODUCT:
                return pb.CREATIVE_MULTI_PRODUCT
            # This default case should never be reached
            case _:
                assert_never(self)


@dataclass
class Targeting:
    """
    A data model to represent possible filters
    """

    qsearch: str | None = None
    filters: dict[str, list[str]] = field(default_factory=dict)
    plids: list[int] = field(default_factory=list)
    cms_page_slug: str | None = None

    @classmethod
    def from_pb(cls, request: pb.Targeting) -> Targeting:
        filters = {}
        if request.filters:
            filters = {key: list(value.values) for key, value in request.filters.items()}

        return Targeting(
            qsearch=request.qsearch,
            filters=filters,
            plids=list(request.plids),
            cms_page_slug=request.cms_page_slug,
        )


@dataclass
class DisplayAdsRequest:
    """
    A data model to represent a display ad S4F protobuf request.
    """

    location: Location
    uuid: str
    platform: Platform
    creatives: list[Creative]
    ad_units: list[str]
    targeting: Targeting
    limit: int
    preview_campaign_id: str | None

    @classmethod
    def from_pb(cls, request: pb.DisplayAdsRequest) -> DisplayAdsRequest:
        return DisplayAdsRequest(
            location=Location(request.location),
            uuid=request.uuid,
            platform=Platform(request.platform),
            creatives=[Creative(c) for c in request.creatives],
            ad_units=list(request.ad_units),
            targeting=Targeting.from_pb(request.targeting),
            limit=request.limit,
            preview_campaign_id=request.preview_campaign_id or None,  # Convert empty PB to None
        )


@dataclass
class DisplayAdsResponse:
    """
    A data model to represent a display ad S4F protobuf response.
    """

    display_ads: list[DisplayAd] = field(default_factory=list)

    def to_pb(self) -> pb.DisplayAdsResponse:
        return pb.DisplayAdsResponse(display_ads=[ad.to_pb() for ad in self.display_ads])


@dataclass
class DisplayAd:
    ad_unit: str
    ad_format: str
    creative: Creative
    tracking_info: TrackingInfo
    value: Banner | SingleProduct | MultiProduct

    def to_pb(self) -> pb.DisplayAd:
        creative = self.creative.to_pb()
        match self.value:
            case Banner(_):
                return pb.DisplayAd(
                    ad_unit=self.ad_unit,
                    creative=creative,
                    tracking=self.tracking_info.to_pb(),
                    banner=self.value.to_pb(),
                    ad_format=self.ad_format,
                )
            case SingleProduct(_):
                return pb.DisplayAd(
                    ad_unit=self.ad_unit,
                    creative=creative,
                    tracking=self.tracking_info.to_pb(),
                    single_product=self.value.to_pb(),
                    ad_format=self.ad_format,
                )
            case MultiProduct(_):
                return pb.DisplayAd(
                    ad_unit=self.ad_unit,
                    creative=creative,
                    tracking=self.tracking_info.to_pb(),
                    multi_product=self.value.to_pb(),
                    ad_format=self.ad_format,
                )
            case _:
                assert_never(self.value)


@dataclass
class ProductAdsRequest:
    """
    A data model to represent a product ad S4F protobuf request.
    """

    location: Location
    uuid: str
    platform: Platform
    targeting: Targeting
    limit: int

    @classmethod
    def from_pb(cls, request: pb.ProductAdsRequest) -> ProductAdsRequest:
        return ProductAdsRequest(
            location=Location(request.location),
            uuid=request.uuid,
            platform=Platform(request.platform),
            targeting=Targeting.from_pb(request.targeting),
            limit=request.limit,
        )


@dataclass
class ProductAdsResponse:
    """
    A data model to represent a product ad S4F protobuf response.
    """

    products: list[ProductAd] = field(default_factory=list)

    def to_pb(self) -> pb.ProductAdsResponse:
        return pb.ProductAdsResponse(products=[pa.to_pb() for pa in self.products])


@dataclass
class Banner:
    background: Background | None
    destination_url: str | None

    def to_pb(self) -> pb.DisplayAd.Banner:
        return pb.DisplayAd.Banner(
            background=self.background.to_pb() if self.background else None,
            destination_url=self.destination_url,
        )


@dataclass
class ProductAd:
    productline_id: int
    variant_id: int | None
    offer_id: int | None
    tracking_info: TrackingInfo

    def to_pb(self) -> pb.ProductAd:
        return pb.ProductAd(
            productline_id=self.productline_id,
            variant_id=self.variant_id,
            offer_id=self.offer_id,
            tracking=self.tracking_info.to_pb(),
        )


@dataclass
class SingleProduct:
    product: ProductAd
    destination_url: str | None

    def to_pb(self) -> pb.DisplayAd.SingleProduct:
        return pb.DisplayAd.SingleProduct(
            product_ad=self.product.to_pb(),
            destination_url=self.destination_url,
        )


@dataclass
class MultiProduct:
    product_ads: list[ProductAd]
    title: str

    def to_pb(self) -> pb.DisplayAd.MultiProduct:
        return pb.DisplayAd.MultiProduct(
            product_ads=[pa.to_pb() for pa in self.product_ads],
            title=self.title,
        )


@dataclass
class Background:
    sm: str
    md: str
    lg: str

    def to_pb(self) -> pb.DisplayAd.Banner.Background:
        return pb.DisplayAd.Banner.Background(
            sm=self.sm,
            md=self.md,
            lg=self.lg,
        )


@dataclass
class TrackingInfo:
    uclid: str
    uuid: str | None
    cli_ubid: str
    seller_id: str | None

    def to_pb(self) -> pb.TrackingInfo:
        return pb.TrackingInfo(
            uclid=self.uclid,
            uuid=self.uuid,
            cli_ubid=self.cli_ubid,
            seller_id=self.seller_id,
        )
