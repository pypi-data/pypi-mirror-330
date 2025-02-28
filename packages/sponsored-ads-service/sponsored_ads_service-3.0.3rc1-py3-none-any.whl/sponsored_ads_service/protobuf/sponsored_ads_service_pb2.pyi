from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

CREATIVE_BANNER: Creative
CREATIVE_MULTI_PRODUCT: Creative
CREATIVE_SINGLE_PRODUCT: Creative
CREATIVE_UNSPECIFIED: Creative
DESCRIPTOR: _descriptor.FileDescriptor
LOCATION_CART: Location
LOCATION_DEALS: Location
LOCATION_HOME: Location
LOCATION_LANDING_PAGE: Location
LOCATION_ORDERS: Location
LOCATION_ORDER_CONFIRMATION: Location
LOCATION_ORDER_DETAILS: Location
LOCATION_ORDER_TRACKING: Location
LOCATION_PDP: Location
LOCATION_SEARCH: Location
LOCATION_UNSPECIFIED: Location
PLATFORM_ANDROID: Platform
PLATFORM_IOS: Platform
PLATFORM_UNSPECIFIED: Platform
PLATFORM_WEB: Platform

class Breakpoints(_message.Message):
    __slots__ = ["medium", "sm"]
    MEDIUM_FIELD_NUMBER: ClassVar[int]
    SM_FIELD_NUMBER: ClassVar[int]
    medium: _containers.RepeatedScalarFieldContainer[int]
    sm: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, sm: Optional[Iterable[int]] = ..., medium: Optional[Iterable[int]] = ...) -> None: ...

class DealsWidget(_message.Message):
    __slots__ = ["position", "results", "title"]
    POSITION_FIELD_NUMBER: ClassVar[int]
    RESULTS_FIELD_NUMBER: ClassVar[int]
    TITLE_FIELD_NUMBER: ClassVar[int]
    position: int
    results: _containers.RepeatedScalarFieldContainer[str]
    title: WidgetTitle
    def __init__(self, title: Optional[Union[WidgetTitle, Mapping]] = ..., position: Optional[int] = ..., results: Optional[Iterable[str]] = ...) -> None: ...

class DisplayAd(_message.Message):
    __slots__ = ["ad_format", "ad_unit", "banner", "creative", "multi_product", "single_product", "tracking"]
    class Banner(_message.Message):
        __slots__ = ["background", "destination_url"]
        class Background(_message.Message):
            __slots__ = ["lg", "md", "sm"]
            LG_FIELD_NUMBER: ClassVar[int]
            MD_FIELD_NUMBER: ClassVar[int]
            SM_FIELD_NUMBER: ClassVar[int]
            lg: str
            md: str
            sm: str
            def __init__(self, sm: Optional[str] = ..., md: Optional[str] = ..., lg: Optional[str] = ...) -> None: ...
        BACKGROUND_FIELD_NUMBER: ClassVar[int]
        DESTINATION_URL_FIELD_NUMBER: ClassVar[int]
        background: DisplayAd.Banner.Background
        destination_url: str
        def __init__(self, background: Optional[Union[DisplayAd.Banner.Background, Mapping]] = ..., destination_url: Optional[str] = ...) -> None: ...
    class MultiProduct(_message.Message):
        __slots__ = ["product_ads", "title"]
        PRODUCT_ADS_FIELD_NUMBER: ClassVar[int]
        TITLE_FIELD_NUMBER: ClassVar[int]
        product_ads: _containers.RepeatedCompositeFieldContainer[ProductAd]
        title: str
        def __init__(self, product_ads: Optional[Iterable[Union[ProductAd, Mapping]]] = ..., title: Optional[str] = ...) -> None: ...
    class SingleProduct(_message.Message):
        __slots__ = ["destination_url", "product_ad"]
        DESTINATION_URL_FIELD_NUMBER: ClassVar[int]
        PRODUCT_AD_FIELD_NUMBER: ClassVar[int]
        destination_url: str
        product_ad: ProductAd
        def __init__(self, product_ad: Optional[Union[ProductAd, Mapping]] = ..., destination_url: Optional[str] = ...) -> None: ...
    AD_FORMAT_FIELD_NUMBER: ClassVar[int]
    AD_UNIT_FIELD_NUMBER: ClassVar[int]
    BANNER_FIELD_NUMBER: ClassVar[int]
    CREATIVE_FIELD_NUMBER: ClassVar[int]
    MULTI_PRODUCT_FIELD_NUMBER: ClassVar[int]
    SINGLE_PRODUCT_FIELD_NUMBER: ClassVar[int]
    TRACKING_FIELD_NUMBER: ClassVar[int]
    ad_format: str
    ad_unit: str
    banner: DisplayAd.Banner
    creative: Creative
    multi_product: DisplayAd.MultiProduct
    single_product: DisplayAd.SingleProduct
    tracking: TrackingInfo
    def __init__(self, ad_unit: Optional[str] = ..., creative: Optional[Union[Creative, str]] = ..., tracking: Optional[Union[TrackingInfo, Mapping]] = ..., banner: Optional[Union[DisplayAd.Banner, Mapping]] = ..., single_product: Optional[Union[DisplayAd.SingleProduct, Mapping]] = ..., multi_product: Optional[Union[DisplayAd.MultiProduct, Mapping]] = ..., ad_format: Optional[str] = ...) -> None: ...

class DisplayAdsRequest(_message.Message):
    __slots__ = ["ad_units", "creatives", "limit", "location", "platform", "preview_campaign_id", "targeting", "uuid"]
    AD_UNITS_FIELD_NUMBER: ClassVar[int]
    CREATIVES_FIELD_NUMBER: ClassVar[int]
    LIMIT_FIELD_NUMBER: ClassVar[int]
    LOCATION_FIELD_NUMBER: ClassVar[int]
    PLATFORM_FIELD_NUMBER: ClassVar[int]
    PREVIEW_CAMPAIGN_ID_FIELD_NUMBER: ClassVar[int]
    TARGETING_FIELD_NUMBER: ClassVar[int]
    UUID_FIELD_NUMBER: ClassVar[int]
    ad_units: _containers.RepeatedScalarFieldContainer[str]
    creatives: _containers.RepeatedScalarFieldContainer[Creative]
    limit: int
    location: Location
    platform: Platform
    preview_campaign_id: str
    targeting: Targeting
    uuid: str
    def __init__(self, location: Optional[Union[Location, str]] = ..., uuid: Optional[str] = ..., platform: Optional[Union[Platform, str]] = ..., creatives: Optional[Iterable[Union[Creative, str]]] = ..., ad_units: Optional[Iterable[str]] = ..., targeting: Optional[Union[Targeting, Mapping]] = ..., limit: Optional[int] = ..., preview_campaign_id: Optional[str] = ...) -> None: ...

class DisplayAdsResponse(_message.Message):
    __slots__ = ["display_ads"]
    DISPLAY_ADS_FIELD_NUMBER: ClassVar[int]
    display_ads: _containers.RepeatedCompositeFieldContainer[DisplayAd]
    def __init__(self, display_ads: Optional[Iterable[Union[DisplayAd, Mapping]]] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ["name", "values"]
    NAME_FIELD_NUMBER: ClassVar[int]
    VALUES_FIELD_NUMBER: ClassVar[int]
    name: str
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: Optional[str] = ..., values: Optional[Iterable[str]] = ...) -> None: ...

class FilterValues(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: Optional[Iterable[str]] = ...) -> None: ...

class ImageNotice(_message.Message):
    __slots__ = ["alt_text", "description", "image_url", "key"]
    ALT_TEXT_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: ClassVar[int]
    KEY_FIELD_NUMBER: ClassVar[int]
    alt_text: str
    description: str
    image_url: str
    key: str
    def __init__(self, key: Optional[str] = ..., image_url: Optional[str] = ..., alt_text: Optional[str] = ..., description: Optional[str] = ...) -> None: ...

class Notice(_message.Message):
    __slots__ = ["image_notice", "text_notice"]
    IMAGE_NOTICE_FIELD_NUMBER: ClassVar[int]
    TEXT_NOTICE_FIELD_NUMBER: ClassVar[int]
    image_notice: ImageNotice
    text_notice: TextNotice
    def __init__(self, text_notice: Optional[Union[TextNotice, Mapping]] = ..., image_notice: Optional[Union[ImageNotice, Mapping]] = ...) -> None: ...

class Positions(_message.Message):
    __slots__ = ["apps", "web"]
    APPS_FIELD_NUMBER: ClassVar[int]
    WEB_FIELD_NUMBER: ClassVar[int]
    apps: Breakpoints
    web: Breakpoints
    def __init__(self, apps: Optional[Union[Breakpoints, Mapping]] = ..., web: Optional[Union[Breakpoints, Mapping]] = ...) -> None: ...

class ProductAd(_message.Message):
    __slots__ = ["offer_id", "productline_id", "tracking", "variant_id"]
    OFFER_ID_FIELD_NUMBER: ClassVar[int]
    PRODUCTLINE_ID_FIELD_NUMBER: ClassVar[int]
    TRACKING_FIELD_NUMBER: ClassVar[int]
    VARIANT_ID_FIELD_NUMBER: ClassVar[int]
    offer_id: int
    productline_id: int
    tracking: TrackingInfo
    variant_id: int
    def __init__(self, productline_id: Optional[int] = ..., variant_id: Optional[int] = ..., offer_id: Optional[int] = ..., tracking: Optional[Union[TrackingInfo, Mapping]] = ...) -> None: ...

class ProductAdsRequest(_message.Message):
    __slots__ = ["limit", "location", "platform", "targeting", "uuid"]
    LIMIT_FIELD_NUMBER: ClassVar[int]
    LOCATION_FIELD_NUMBER: ClassVar[int]
    PLATFORM_FIELD_NUMBER: ClassVar[int]
    TARGETING_FIELD_NUMBER: ClassVar[int]
    UUID_FIELD_NUMBER: ClassVar[int]
    limit: int
    location: Location
    platform: Platform
    targeting: Targeting
    uuid: str
    def __init__(self, location: Optional[Union[Location, str]] = ..., uuid: Optional[str] = ..., platform: Optional[Union[Platform, str]] = ..., targeting: Optional[Union[Targeting, Mapping]] = ..., limit: Optional[int] = ...) -> None: ...

class ProductAdsResponse(_message.Message):
    __slots__ = ["products"]
    PRODUCTS_FIELD_NUMBER: ClassVar[int]
    products: _containers.RepeatedCompositeFieldContainer[ProductAd]
    def __init__(self, products: Optional[Iterable[Union[ProductAd, Mapping]]] = ...) -> None: ...

class Targeting(_message.Message):
    __slots__ = ["cms_page_slug", "filters", "plids", "qsearch"]
    class FiltersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: FilterValues
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[FilterValues, Mapping]] = ...) -> None: ...
    CMS_PAGE_SLUG_FIELD_NUMBER: ClassVar[int]
    FILTERS_FIELD_NUMBER: ClassVar[int]
    PLIDS_FIELD_NUMBER: ClassVar[int]
    QSEARCH_FIELD_NUMBER: ClassVar[int]
    cms_page_slug: str
    filters: _containers.MessageMap[str, FilterValues]
    plids: _containers.RepeatedScalarFieldContainer[int]
    qsearch: str
    def __init__(self, qsearch: Optional[str] = ..., filters: Optional[Mapping[str, FilterValues]] = ..., plids: Optional[Iterable[int]] = ..., cms_page_slug: Optional[str] = ...) -> None: ...

class TextNotice(_message.Message):
    __slots__ = ["description", "key", "text"]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    KEY_FIELD_NUMBER: ClassVar[int]
    TEXT_FIELD_NUMBER: ClassVar[int]
    description: str
    key: str
    text: str
    def __init__(self, key: Optional[str] = ..., text: Optional[str] = ..., description: Optional[str] = ...) -> None: ...

class TrackingInfo(_message.Message):
    __slots__ = ["cli_ubid", "seller_id", "uclid", "uuid"]
    CLI_UBID_FIELD_NUMBER: ClassVar[int]
    SELLER_ID_FIELD_NUMBER: ClassVar[int]
    UCLID_FIELD_NUMBER: ClassVar[int]
    UUID_FIELD_NUMBER: ClassVar[int]
    cli_ubid: str
    seller_id: str
    uclid: str
    uuid: str
    def __init__(self, uclid: Optional[str] = ..., uuid: Optional[str] = ..., cli_ubid: Optional[str] = ..., seller_id: Optional[str] = ...) -> None: ...

class WidgetTitle(_message.Message):
    __slots__ = ["text", "text_notices"]
    TEXT_FIELD_NUMBER: ClassVar[int]
    TEXT_NOTICES_FIELD_NUMBER: ClassVar[int]
    text: str
    text_notices: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, text: Optional[str] = ..., text_notices: Optional[Iterable[str]] = ...) -> None: ...

class Location(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Platform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Creative(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
