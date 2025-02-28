from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import TYPE_CHECKING, Any, TypeAlias

from typing_extensions import TypedDict

from sponsored_ads_service.sponsored_ads import models as dto

if TYPE_CHECKING:
    from sponsored_ads_service.models.sponsored_display import AdUnit


class Creative(Enum):
    """
    https://docs.google.com/document/d/1uHmWMcsuDalfkWYnBJDdVRTWIsRFwUwwEHtwouygyz0/edit
    """

    UNKNOWN = "unknown-creative"
    SINGLE_PRODUCT = "single-product"
    MULTI_PRODUCT_3 = "Multi-product-3"
    SEARCH_BANNER = "search-banner"  # migrating to search-banner-top
    SEARCH_BANNER_TOP = "search-banner-top"
    PDP_BANNER = "pdp-banner"
    HOMEPAGE_CAROUSEL_BANNER = "Homepage-carousel-banner"
    HOMEPAGE_RIGHT_HAND_BANNER = "Homepage-Right-hand-banner"
    CATEGORY_CAROUSEL_BANNER = "category-carousel-banner"
    ORDER_PAGE_BANNER = "order-page-banner"
    CART_BANNER = "cart-banner"

    @classmethod
    def _missing_(cls, value: object) -> Creative:
        return Creative.UNKNOWN


@dataclass
class ProductsRequest:
    """The mapped request used to make a sponsored products request to OnlineSales"""

    cli_ubid: str
    device: Device
    pcnt: int
    page_type: SearchPageType
    client_id: str
    a_slot: str
    page_name: str | None = None
    keywords: list[str] = field(default_factory=list)
    min_price: int | None = None
    max_price: int | None = None
    brands: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    sku_ids: list[int] = field(default_factory=list)
    rtl_custom_label_0: list[str] | None = None
    a_type: str = "PRODUCT"
    country: str = "ZA"
    currency: str = "ZAR"
    language: str = "en"

    def to_request_params(self) -> dict:
        data = {
            "cli_ubid": self.cli_ubid,
            "device": self.device.value,
            "pcnt": self.pcnt,
            "page_type": self.page_type.value if self.page_type else None,
            "client_id": self.client_id,
            "a_slot": self.a_slot,
            "page_name": self.page_name,
            "keywords[]": self.keywords if self.keywords else None,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "brands[]": self.brands if self.brands else None,
            "categories[]": self.categories if self.categories else None,
            "sku_ids[]": self.sku_ids if self.sku_ids else None,
            "rtl_custom_label_0": self.rtl_custom_label_0 if self.rtl_custom_label_0 else None,
            "a_type": self.a_type,
            "country": self.country,
            "currency": self.currency,
            "language": self.language,
        }
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class ProductsResponse:
    """A data model for the response from a sponsored products request to OnlineSales"""

    products: list[Product]


class DisplayAdPageType(Enum):
    """
    Display page type values that may be passed to the OnlineSales Display Ads
    endpoint `pt` parameter.
    """

    PDP = "PRODUCT_PAGE"
    SEARCH = "SEARCH_PAGE"
    HOME = "HOME_PAGE"
    CATEGORY = "CATEGORY_PAGE"
    ORDERS = "ORDER_LIST_PAGE"
    ORDER_DETAILS = "ORDER_DETAILS_PAGE"
    ORDER_TRACKING = "ORDER_TRACKING_PAGE"
    ORDER_CONFIRMATION = "ORDER_CONFIRMATION_PAGE"
    CART = "CART_PAGE"

    @classmethod
    def from_location(cls, location: dto.Location) -> DisplayAdPageType:
        """
        Map from a location to a DisplayAdPageType
        :param location:
        :return:
        """
        match location:
            case dto.Location.PDP:
                return DisplayAdPageType.PDP
            case dto.Location.SEARCH:
                return DisplayAdPageType.SEARCH
            case dto.Location.HOME:
                return DisplayAdPageType.HOME
            case dto.Location.LANDING_PAGE:
                return DisplayAdPageType.CATEGORY
            case dto.Location.ORDERS:
                return DisplayAdPageType.ORDERS
            case dto.Location.ORDER_DETAILS:
                return DisplayAdPageType.ORDER_DETAILS
            case dto.Location.ORDER_TRACKING:
                return DisplayAdPageType.ORDER_TRACKING
            case dto.Location.ORDER_CONFIRMATION:
                return DisplayAdPageType.ORDER_CONFIRMATION
            case dto.Location.CART:
                return DisplayAdPageType.CART
            case _:
                raise ValueError(f"Location {location} not supported")


class SearchPageType(Enum):
    """
    Search page type values that may be passed to the OnlineSales Product Ads
    endpoint `pt` parameter.
    """

    CATEGORY = "CATEGORY"
    CUSTOM = "CUSTOM"
    HOME = "HOME"
    PRODUCT = "PRODUCT"
    SEARCH = "SEARCH"


class Device(Enum):
    """
    Device category values that may be passed to the OnlineSales Display Ads endpoint
    `device` parameter.
    """

    ANDROID = "android"
    DESKTOP = "desktop"
    IOS = "ios"

    @classmethod
    def from_platform(cls, platform: dto.Platform) -> Device:
        """
        Map from a platform to a Device
        :param platform: The request platform
        :return: A Device recognised by OnlineSales
        """
        match platform:
            case dto.Platform.ANDROID:
                return cls.ANDROID
            case dto.Platform.WEB:
                return cls.DESKTOP
            case dto.Platform.IOS:
                return cls.IOS
            case _:
                return cls.DESKTOP


class FilterKey(Enum):
    """
    The OnlineSales Display Ads endpoint accepts filter parameters in the format
    `f.<key> = value`. This class defines acceptable `key` values.
    """

    BRAND = "brand"
    CATEGORIES = "category"
    KEYWORD = "keyword"
    SKU = "sku_id"


FilterPairs: TypeAlias = dict[FilterKey, Any]  # Convenience type alias


@dataclass
class DisplayRequest:
    """Model represents the parameters of an HTTP request to the OnlineSales API
    `<os-given-sub-domain>.o-s.io/bsda?` Display Ads endpoint

    See https://developers.onlinesales.ai/reference/sda-examples
    """

    client_id: str  # Retailer unique id shared by onlinesales.ai
    device_id: str  # Retailers Generated Id to identify unique shopper
    page_type: DisplayAdPageType  # page type from which the request is made
    device: Device  # Device category
    ad_units: list[AdUnit] = field(default_factory=list)
    creatives: list[Creative] = field(default_factory=list)
    filters: FilterPairs = field(default_factory=dict)
    preview_campaign_id: str | None = None

    def to_request_params(self) -> dict:
        """
        Create and return a dict that can be used as API client parameters

        See https://developers.onlinesales.ai/reference/sda-examples
        Example:
        https://tal-ba.o-s.io/v2/bsda?ad_type=brand_ads&client_id=127150\
            &device_id=a4f892126245&pt=SEARCH_PAGE&au[]=search-top\
            &rn=0.09818990581288844&device=mobile&f.keyword=Gin
        """

        data = {
            "ad_type": "brand_ads",
            "client_id": self.client_id,
            "device_id": self.device_id,
            "pt": self.page_type.value,
            "au[]": self.ad_units,
            "crt[]": [c.value for c in self.creatives],
            "rn": random.uniform(0, 1),  # Random number to avoid browser caching
            "f.device": self.device.value,
        }
        if self.filters:
            for k, v in self.filters.items():
                if k == FilterKey.CATEGORIES:
                    # Categories need a different treatment
                    for i, c in enumerate(v, 1):
                        data[f"f.{k.value}_l{i}"] = c
                else:
                    data[f"f.{k.value}"] = v

        if self.preview_campaign_id:
            # Yes the remote side uses a shorter name
            data["campaign_id"] = self.preview_campaign_id

        return {k: v for k, v in data.items() if v}


@dataclass
class Display:
    """
    Model represents an item in the OnlineSales `.ads[]` response array

    This model is fairly "naive", and used as a container for the API response as-given.
    The data is refined further, when transformed to a `SponsoredDisplayAd` instance.
    """

    ad_type: str  # Constant string identifier for ad type (banner/product)
    client_id: str
    ad_unit: str
    uclid: str
    creative: Creative
    destination_url: str = ""
    products: list[Product] = field(default_factory=list)
    images: dict[str, str] = field(default_factory=dict)


@dataclass
class DisplayResponse:
    """A data model for the response from a sponsored display request to OnlineSales"""

    ads: list[Display]


class ResponseDisplayObject(TypedDict):
    """API response object type"""

    client_id: int
    au: str
    uclid: str
    crt: str
    elements: ResponseElements


class ResponseElements(TypedDict, total=False):
    """
    Typing for OnlineSales API display ads response `ads[].elements`
    """

    ad_type: str
    landing_product_list: list[ProductElement]  # Banner ads contain this key
    product_list: list[ProductElement]  # Product ads contain this key
    destination_url: str  # OS Display Ads contains this key

    # Banner ads contain further fields for background images, usually of the form
    # bg_img_src_123x456, but are defined in MAP_ONLINESALES_CREATIVE_BANNER_IMAGE_SIZES.
    # The fields are discovered if they have "_img_" in their name.


class ProductElement(TypedDict, total=False):
    sku_id: str
    tsin: str
    plid: str
    seller_id: str
    uclid: str  # landing_product_list results not have this property


@dataclass
class Product:
    """A single OnlineSales product returned from the sponsored products request"""

    uclid: str
    sku_id: int
    plid: int
    seller_id: str
    tsin: int | None = None


class Breakpoint(StrEnum):
    # **Note** the order here is important, *DO NOT CHANGE THESE*

    SMALL = "sm"
    MEDIUM = "md"
    LARGE = "lg"
