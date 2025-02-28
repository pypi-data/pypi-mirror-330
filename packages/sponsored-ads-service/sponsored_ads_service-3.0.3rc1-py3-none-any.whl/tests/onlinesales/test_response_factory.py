import pytest

from sponsored_ads_service.errors import SponsoredAdsServiceError
from sponsored_ads_service.onlinesales import models as os
from sponsored_ads_service.sponsored_ads.models import (
    Background,
    Banner,
    Creative,
    DisplayAd,
    DisplayAdsResponse,
    ProductAd,
    ProductAdsResponse,
    TrackingInfo,
)


@pytest.fixture
def response_factory(mocker, config):
    from sponsored_ads_service.onlinesales import ResponseFactory

    destination_url_factory = mocker.Mock()
    destination_url_factory.from_display_ad.return_value = "https://www.test.com"
    return ResponseFactory(config=config, destination_url_factory=destination_url_factory)


@pytest.mark.parametrize(
    ("value", "expected_creative"),
    [
        (
            os.Display(
                ad_type="banner",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.PDP_BANNER,
                destination_url="https://www.test.com",
                products=[],
                images={
                    "bg_img_src_300x250": "https://www.test.com/img?300x250",
                    "bg_img_src_300x50": "https://www.test.com/img?300x50",
                    "bg_img_src_728x90": "https://www.test.com/img?728x90",
                    "bg_img_src_1292x120": "https://www.test.com/img?1292x120",
                },
            ),
            Creative.BANNER,
        ),
        (
            os.Display(
                ad_type="single-product",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.SINGLE_PRODUCT,
                destination_url="https://www.test.com",
                products=[
                    os.Product(
                        uclid="",
                        sku_id=93651156,
                        plid=72579690,
                        seller_id="R11434",
                        tsin=69311566,
                    )
                ],
            ),
            Creative.SINGLE_PRODUCT,
        ),
        (
            os.Display(
                ad_type="single-product",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.MULTI_PRODUCT_3,
                destination_url="https://www.test.com",
                products=[
                    os.Product(
                        uclid="",
                        sku_id=3001,
                        plid=2001,
                        seller_id="R100",
                        tsin=3001,
                    ),
                    os.Product(
                        uclid="",
                        sku_id=3002,
                        plid=2002,
                        seller_id="R200",
                        tsin=2001,
                    ),
                ],
            ),
            Creative.MULTI_PRODUCT,
        ),
    ],
)
def test_display_ad_from_dict(response_factory, value, expected_creative):
    display_ad = response_factory._build_display_ad(value, "test_uuid")
    assert display_ad.creative == expected_creative


def test_display_ad_from_dict_unknown_creative(response_factory):
    with pytest.raises(SponsoredAdsServiceError):
        response_factory._build_display_ad(
            os.Display(
                ad_type="banner",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.UNKNOWN,
                destination_url="https://www.test.com",
                products=[],
                images={
                    "bg_img_src_300x250": "https://www.test.com/img?300x250",
                    "bg_img_src_300x50": "https://www.test.com/img?300x50",
                    "bg_img_src_728x90": "https://www.test.com/img?728x90",
                    "bg_img_src_1292x120": "https://www.test.com/img?1292x120",
                },
            ),
            "test_uuid",
        )


def test_product_ads_response_from_dict(response_factory):
    os_response = os.ProductsResponse(
        products=[
            os.Product(
                uclid="",
                sku_id=3001,
                plid=1001,
                seller_id="R100",
                tsin=2001,
            ),
            os.Product(
                uclid="",
                sku_id=3002,
                plid=1002,
                seller_id="R200",
                tsin=2002,
            ),
        ]
    )

    expected = ProductAdsResponse(
        products=[
            ProductAd(
                productline_id=1001,
                variant_id=2001,
                offer_id=3001,
                tracking_info=TrackingInfo(
                    uclid="",
                    uuid=None,
                    cli_ubid="test_uuid",
                    seller_id="R100",
                ),
            ),
            ProductAd(
                productline_id=1002,
                variant_id=2002,
                offer_id=3002,
                tracking_info=TrackingInfo(
                    uclid="",
                    uuid=None,
                    cli_ubid="test_uuid",
                    seller_id="R200",
                ),
            ),
        ]
    )
    assert response_factory.build_product_ad_response(os_response, "test_uuid") == expected


def test_display_ads_response_from_dict(response_factory):
    os_response = os.DisplayResponse(
        ads=[
            os.Display(
                ad_type="banner",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.PDP_BANNER,
                destination_url="https://www.test.com",
                products=[],
                images={
                    "bg_img_src_300x250": "https://www.test.com/img?300x250",
                    "bg_img_src_300x50": "https://www.test.com/img?300x50",
                    "bg_img_src_728x90": "https://www.test.com/img?728x90",
                    "bg_img_src_1292x120": "https://www.test.com/img?1292x120",
                },
            ),
        ]
    )
    expected = DisplayAdsResponse(
        display_ads=[
            DisplayAd(
                ad_unit="pdp-slot-1",
                creative=Creative.BANNER,
                tracking_info=TrackingInfo(
                    uclid="2|67890|67890",
                    uuid="198501",
                    cli_ubid="test_cli_ubid",
                    seller_id=None,
                ),
                value=Banner(
                    background=Background(
                        sm="https://www.test.com/img?300x250",
                        md="https://www.test.com/img?300x250",
                        lg="https://www.test.com/img?300x250",
                    ),
                    destination_url="https://www.test.com",
                ),
                ad_format="pdp-banner",
            )
        ]
    )
    assert response_factory.build_display_ad_response(os_response, "test_cli_ubid") == expected
