import pytest

from sponsored_ads_service.models.onlinesales import (
    Device,
    DisplayAdPageType,
    FilterKey,
    OnlineSalesCreative,
    OnlineSalesDisplayRequest,
    OnlineSalesProductsRequest,
    SearchPageType,
)

pytestmark = pytest.mark.models

RANDOM_UNIFORM = 0.030709420884512673


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        (
            OnlineSalesProductsRequest(
                cli_ubid="1234",
                device="desktop",
                pcnt=5,
                page_type=SearchPageType.SEARCH,
                client_id="5678",
                a_slot="1",
            ),
            {
                "cli_ubid": "1234",
                "device": "desktop",
                "pcnt": 5,
                "page_type": "SEARCH",
                "client_id": "5678",
                "a_slot": "1",
                "a_type": "PRODUCT",
                "country": "ZA",
                "currency": "ZAR",
                "language": "en",
            },
        ),
        (
            OnlineSalesProductsRequest(
                cli_ubid="1234",
                device="desktop",
                pcnt=5,
                page_type=SearchPageType.SEARCH,
                client_id="5678",
                a_slot="1",
                keywords=["word", "other"],
            ),
            {
                "cli_ubid": "1234",
                "device": "desktop",
                "pcnt": 5,
                "page_type": "SEARCH",
                "client_id": "5678",
                "a_slot": "1",
                "keywords[]": ["word", "other"],
                "a_type": "PRODUCT",
                "country": "ZA",
                "currency": "ZAR",
                "language": "en",
            },
        ),
        (
            OnlineSalesProductsRequest(
                cli_ubid="1234",
                device="desktop",
                pcnt=5,
                page_type=SearchPageType.SEARCH,
                client_id="5678",
                a_slot="1",
                keywords=[],
                brands=["Sony", "Canon"],
                min_price=None,
            ),
            {
                "cli_ubid": "1234",
                "device": "desktop",
                "pcnt": 5,
                "page_type": "SEARCH",
                "client_id": "5678",
                "a_slot": "1",
                "brands[]": ["Sony", "Canon"],
                "a_type": "PRODUCT",
                "country": "ZA",
                "currency": "ZAR",
                "language": "en",
            },
        ),
        (
            OnlineSalesDisplayRequest(
                client_id="123456",
                ad_units=["search-top", "pdp-slot-1"],
                device_id="890",
                page_type=DisplayAdPageType.SEARCH,
                device=Device.DESKTOP,
                filters={
                    FilterKey.BRAND: "Canon",
                    FilterKey.CATEGORIES: [
                        "Cameras",
                        "Cameras & Lenses",
                        "Camera Accessories",
                    ],
                },
            ),
            {
                "ad_type": "brand_ads",
                "au[]": ["search-top", "pdp-slot-1"],
                "client_id": "123456",
                "f.device": "desktop",
                "device_id": "890",
                "f.category_l1": "Cameras",
                "f.category_l2": "Cameras & Lenses",
                "f.category_l3": "Camera Accessories",
                "f.brand": "Canon",
                "pt": "SEARCH_PAGE",
                "rn": RANDOM_UNIFORM,
            },
        ),
        (
            OnlineSalesDisplayRequest(
                client_id="123456",
                device_id="890",
                page_type=DisplayAdPageType.PDP,
                device=Device.ANDROID,
            ),
            {
                "ad_type": "brand_ads",
                "client_id": "123456",
                "device_id": "890",
                "pt": "PRODUCT_PAGE",
                "rn": RANDOM_UNIFORM,
                "f.device": "android",
            },
        ),
    ],
)
def test_to_request_params(mocker, model, expected):
    mocker.patch("random.uniform", return_value=RANDOM_UNIFORM)

    assert model.to_request_params() == expected


def test_online_sales_creative_missing():
    v = OnlineSalesCreative("qqqqqqq")
    assert v == OnlineSalesCreative.UNKNOWN
