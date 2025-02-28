from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING

from typing_extensions import TypedDict

from sponsored_ads_service.errors import BadRequestError, SponsoredDisplayMissingBannerError
from sponsored_ads_service.onlinesales import models as os
from sponsored_ads_service.sponsored_ads import models as dto

if TYPE_CHECKING:
    from sponsored_ads_service.configuration import SponsoredAdsConfig


class DisplayBannerMap(TypedDict):
    """
    Map the image size keys we want to send to frontends to the keys we expect
    to receive from OnlineSales. This allows us to just map it directly and not care
    what the format of the field name is and not rely on string parsing and sorting
    to do this mapping.

    Using a TypedDict to make it easier to iterate and find items here
    based on the Breakpoint enum (same field names as used in that enum)
    """

    sm: str
    md: str
    lg: str


"""
The map below controls which fields from OnlineSales will be used for which banner
size. We reuse some fields for more than one size in some cases.

`search-banner` is migrating to `search-banner-top` and `search-banner` can eventually
be removed.
"""
_MAP_ONLINESALES_CREATIVE_BANNER_IMAGE_SIZES = {
    os.Creative.SEARCH_BANNER: DisplayBannerMap(
        sm="bg_img_src_300x50",
        md="bg_img_src_728x90",
        lg="bg_img_src_1292x120",
    ),
    os.Creative.SEARCH_BANNER_TOP: DisplayBannerMap(
        sm="bg_img_src_320x100",
        md="bg_img_src_728x90",
        lg="bg_img_src_1292x120",
    ),
    os.Creative.PDP_BANNER: DisplayBannerMap(
        sm="bg_img_src_300x250",
        md="bg_img_src_300x250",
        lg="bg_img_src_300x250",
    ),
    os.Creative.HOMEPAGE_RIGHT_HAND_BANNER: DisplayBannerMap(
        sm="bg_img_src_300x355",
        md="bg_img_src_300x355",
        lg="bg_img_src_300x355",
    ),
    os.Creative.HOMEPAGE_CAROUSEL_BANNER: DisplayBannerMap(
        sm="bg_img_src_1200x1000",
        md="bg_img_src_1292x300",
        lg="bg_img_src_1292x300",
    ),
    os.Creative.CATEGORY_CAROUSEL_BANNER: DisplayBannerMap(
        sm="bg_img_src_1200x1000",
        md="bg_img_src_1292x300",
        lg="bg_img_src_1292x300",
    ),
    os.Creative.ORDER_PAGE_BANNER: DisplayBannerMap(
        sm="bg_img_src_320x100",
        md="bg_img_src_728x90",
        lg="bg_img_src_970x90",
    ),
    os.Creative.CART_BANNER: DisplayBannerMap(
        sm="bg_img_src_320x100",
        md="bg_img_src_728x90",
        lg="bg_img_src_1292x120",
    ),
}


class CreativeFactory:
    def __init__(self, config: SponsoredAdsConfig) -> None:
        self._config = config

        self._creatives_map_to_client: dict[os.Creative, dto.Creative] = {
            os.Creative.SEARCH_BANNER: dto.Creative.BANNER,
            os.Creative.PDP_BANNER: dto.Creative.BANNER,
            os.Creative.HOMEPAGE_RIGHT_HAND_BANNER: dto.Creative.BANNER,
            os.Creative.HOMEPAGE_CAROUSEL_BANNER: dto.Creative.BANNER,
            os.Creative.CATEGORY_CAROUSEL_BANNER: dto.Creative.BANNER,
            os.Creative.SINGLE_PRODUCT: dto.Creative.SINGLE_PRODUCT,
            os.Creative.MULTI_PRODUCT_3: dto.Creative.MULTI_PRODUCT,
            os.Creative.ORDER_PAGE_BANNER: dto.Creative.BANNER,
            os.Creative.CART_BANNER: dto.Creative.BANNER,
        }
        self._creatives_map_to_onlinesales: dict[
            dto.Location, dict[dto.Creative, list[os.Creative]]
        ] = {
            dto.Location.SEARCH: {
                dto.Creative.BANNER: [os.Creative.SEARCH_BANNER],
                dto.Creative.SINGLE_PRODUCT: [os.Creative.SINGLE_PRODUCT],
                dto.Creative.MULTI_PRODUCT: [os.Creative.MULTI_PRODUCT_3],
            },
            dto.Location.PDP: {
                dto.Creative.BANNER: [os.Creative.PDP_BANNER],
                dto.Creative.SINGLE_PRODUCT: [os.Creative.SINGLE_PRODUCT],
            },
            dto.Location.HOME: {
                dto.Creative.BANNER: [
                    os.Creative.HOMEPAGE_CAROUSEL_BANNER,
                    os.Creative.HOMEPAGE_RIGHT_HAND_BANNER,
                ],
            },
            dto.Location.LANDING_PAGE: {
                dto.Creative.BANNER: [os.Creative.CATEGORY_CAROUSEL_BANNER]
            },
            dto.Location.ORDERS: {dto.Creative.BANNER: [os.Creative.ORDER_PAGE_BANNER]},
            dto.Location.ORDER_DETAILS: {dto.Creative.BANNER: [os.Creative.ORDER_PAGE_BANNER]},
            dto.Location.ORDER_TRACKING: {dto.Creative.BANNER: [os.Creative.ORDER_PAGE_BANNER]},
            dto.Location.ORDER_CONFIRMATION: {
                dto.Creative.BANNER: [os.Creative.ORDER_PAGE_BANNER]
            },
            dto.Location.CART: {dto.Creative.BANNER: [os.Creative.CART_BANNER]},
        }

        if self._config.get_rollout_flag_search_banner_remap():
            # Don't let old creatives go back pretending to be the new type.
            self._creatives_map_to_client.pop(os.Creative.SEARCH_BANNER, None)
            # Replace the old mapping
            self._creatives_map_to_client[os.Creative.SEARCH_BANNER_TOP] = dto.Creative.BANNER
            self._creatives_map_to_onlinesales[dto.Location.SEARCH][dto.Creative.BANNER] = [
                os.Creative.SEARCH_BANNER_TOP
            ]

    def from_request_creatives(
        self, creatives: list[dto.Creative], /, *, location: dto.Location
    ) -> list[os.Creative]:
        try:
            return list(
                chain.from_iterable(
                    self._creatives_map_to_onlinesales[location][creative]
                    for creative in creatives
                )
            )
        except KeyError as e:
            raise BadRequestError("Unsupported creative and page type combination") from e

    def from_onlinesales_creative(self, creative: os.Creative) -> dto.Creative:
        return self._creatives_map_to_client.get(creative, dto.Creative.UNSPECIFIED)

    @classmethod
    def build_images(
        cls, creative: os.Creative, onlinesales_images: dict[str, str]
    ) -> dto.Background | None:
        """
        Build and return a dictionary containing banner image sources for three breakpoints.
        """

        banner_map = _MAP_ONLINESALES_CREATIVE_BANNER_IMAGE_SIZES.get(creative)
        if not banner_map:
            return None

        result = {}
        for bp in os.Breakpoint:
            m = banner_map[bp.value]
            image_url = onlinesales_images.get(m)
            if not image_url:
                # We expect all images for a given creative to be present
                raise SponsoredDisplayMissingBannerError(
                    f"Cannot find image '{m}' for creative '{creative}'"
                )
            result[bp.value] = image_url

        return dto.Background(**result)
