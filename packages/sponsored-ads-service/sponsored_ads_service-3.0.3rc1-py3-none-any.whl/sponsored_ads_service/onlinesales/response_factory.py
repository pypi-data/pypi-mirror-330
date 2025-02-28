from typing import assert_never

from sponsored_ads_service.configuration import SponsoredAdsConfig
from sponsored_ads_service.errors import SponsoredAdsServiceError
from sponsored_ads_service.onlinesales import CreativeFactory
from sponsored_ads_service.onlinesales.destination_url_factory import DestinationUrlFactory
from sponsored_ads_service.onlinesales.models import (
    Creative,
    Display,
    DisplayResponse,
    Product,
    ProductsResponse,
)
from sponsored_ads_service.sponsored_ads.models import (
    Background,
    Banner,
    DisplayAd,
    DisplayAdsResponse,
    MultiProduct,
    ProductAd,
    ProductAdsResponse,
    SingleProduct,
    TrackingInfo,
)
from sponsored_ads_service.sponsored_ads.models import (
    Creative as dto_Creative,
)


class ResponseFactory:
    def __init__(
        self, config: SponsoredAdsConfig, destination_url_factory: DestinationUrlFactory
    ) -> None:
        self._config = config
        self._creative_factory = CreativeFactory(config)
        self._destination_url_factory = destination_url_factory

    def build_product_ad_response(
        self, os_response: ProductsResponse, uuid: str
    ) -> ProductAdsResponse:
        return ProductAdsResponse(
            products=[self._build_product_ad(product, uuid) for product in os_response.products]
        )

    def build_display_ad_response(
        self, os_response: DisplayResponse, cli_ubid: str
    ) -> DisplayAdsResponse:
        ads = [self._build_display_ad(ad, cli_ubid) for ad in os_response.ads]
        return DisplayAdsResponse(display_ads=[da for da in ads if da])

    def _build_display_ad(self, os_response: Display, cli_ubid: str) -> DisplayAd | None:
        creative = self._creative_factory.from_onlinesales_creative(os_response.creative)
        tracking_info = self._build_tracking_info(os_response, cli_ubid)
        value: Banner | SingleProduct | MultiProduct
        match creative:
            case dto_Creative.BANNER:
                value = self._build_banner(os_response)
            case dto_Creative.SINGLE_PRODUCT:
                value = self._build_single_product_ad(os_response, cli_ubid)
            case dto_Creative.MULTI_PRODUCT:
                value = self._build_multi_product_ad(os_response, cli_ubid)
            case dto_Creative.UNSPECIFIED:
                raise SponsoredAdsServiceError("Creative type is unspecified")
            case _:
                assert_never(creative)

        return DisplayAd(
            ad_unit=os_response.ad_unit,
            ad_format=os_response.creative.value,
            creative=creative,
            tracking_info=tracking_info,
            value=value,
        )

    def _build_single_product_ad(self, os_response: Display, uuid: str) -> SingleProduct:
        return SingleProduct(
            product=self._build_product_ad(os_response.products[0], uuid),
            destination_url=self._destination_url_factory.from_display_ad(os_response),
        )

    def _build_multi_product_ad(self, os_response: Display, uuid: str) -> MultiProduct:
        product_ads = [self._build_product_ad(product, uuid) for product in os_response.products]
        return MultiProduct(
            product_ads=[pa for pa in product_ads if pa is not None],
            title=SponsoredAdsConfig().get_widget_product_title(),
        )

    def _build_product_ad(self, os_response: Product, uuid: str) -> ProductAd:
        return ProductAd(
            productline_id=os_response.plid,
            variant_id=os_response.tsin,
            offer_id=os_response.sku_id,
            tracking_info=self._build_tracking_info(os_response, uuid),
        )

    def _build_banner(self, os_response: Display) -> Banner:
        return Banner(
            background=self._build_background(os_response.creative, os_response.images),
            destination_url=self._destination_url_factory.from_display_ad(os_response),
        )

    def _build_background(self, creative: Creative, os_images: dict) -> Background | None:
        return self._creative_factory.build_images(creative, os_images)

    def _build_tracking_info(self, os_response: Product | Display, cli_ubid: str) -> TrackingInfo:
        uuid = os_response.client_id if isinstance(os_response, Display) else None
        seller_id = os_response.seller_id if isinstance(os_response, Product) else None
        return TrackingInfo(
            uclid=os_response.uclid,
            uuid=uuid,
            cli_ubid=cli_ubid,
            seller_id=seller_id,
        )
