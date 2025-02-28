from contextlib import nullcontext
from unittest.mock import MagicMock

import pytest
from circuitbreaker.breaker import CircuitBreaker
from pytest_lazy_fixtures import lf
from rest_clients.exceptions import TimeoutException

from sponsored_ads_service.configuration import SponsoredAdsConfig
from sponsored_ads_service.configuration.sponsored_ads_config import CircuitBreakerConfig
from sponsored_ads_service.errors import DownstreamError
from sponsored_ads_service.models.onlinesales import SearchPageType
from sponsored_ads_service.onlinesales import OnlinesalesFacade, ResponseFactory
from sponsored_ads_service.onlinesales.models import (
    Device,
    DisplayAdPageType,
    DisplayRequest,
    FilterKey,
    ProductsRequest,
)
from sponsored_ads_service.sponsored_ads.models import (
    Creative,
    DisplayAd,
    DisplayAdsResponse,
    ProductAd,
    ProductAdsResponse,
    SingleProduct,
    TrackingInfo,
)


@pytest.fixture
def mock_config():
    return MagicMock()


@pytest.fixture
def mock_stats_client():
    return MagicMock()


@pytest.fixture
def mock_clients():
    return MagicMock()


@pytest.fixture
def mock_display_client():
    display_client = MagicMock()
    display_client.get_display_ads = MagicMock()
    return display_client


@pytest.fixture
def mock_products_client():
    products_client = MagicMock()
    products_client.get_products_ads = MagicMock()
    return products_client


@pytest.fixture
def mock_creative_factory():
    return MagicMock()


@pytest.fixture
def mock_factory():
    return MagicMock()


@pytest.mark.parametrize(
    ("enabled", "expected_contextmanager"),
    [
        (True, CircuitBreaker),
        (False, nullcontext),
    ],
)
def test_get_onlinesales_request_context_for_circuitbreaker_enabled(
    mocker,
    enabled,
    expected_contextmanager,
    mock_creative_factory,
    mock_products_client,
    mock_display_client,
    mock_clients,
    mock_stats_client,
    mock_config,
):
    from sponsored_ads_service.onlinesales import OnlinesalesFacade

    mock_config = mocker.MagicMock(spec=SponsoredAdsConfig)
    mock_config.get_circuitbreaker_config.return_value = CircuitBreakerConfig(
        enabled=enabled, reset_timeout_s=5, max_fail=3
    )
    facade = OnlinesalesFacade(
        config=mock_config,
        stats_client=mock_stats_client,
        display_client=mock_display_client,
        products_client=mock_products_client,
        response_factory=mocker.MagicMock(),
    )
    output = facade._get_onlinesales_request_context(
        page_type=SearchPageType.SEARCH, preview_mode=False
    )

    assert isinstance(output, expected_contextmanager)


@pytest.mark.parametrize(
    ("preview_mode", "expected_signature"),
    [
        (True, "onlinesales.onlinesales_request_context_search_preview.get"),
        (False, "onlinesales.onlinesales_request_context_search.get"),
    ],
)
def test_get_onlinesales_request_context_for_circuitbreaker_preview(
    mocker,
    preview_mode,
    expected_signature,
    mock_creative_factory,
    mock_products_client,
    mock_display_client,
    mock_clients,
    mock_stats_client,
    mock_config,
):
    from sponsored_ads_service.onlinesales import OnlinesalesFacade

    mock_config = mocker.MagicMock(spec=SponsoredAdsConfig)
    mock_config.get_circuitbreaker_config.return_value = CircuitBreakerConfig(
        enabled=True, reset_timeout_s=5, max_fail=3
    )
    facade = OnlinesalesFacade(
        config=mock_config,
        stats_client=mock_stats_client,
        display_client=mock_display_client,
        products_client=mock_products_client,
        response_factory=mocker.MagicMock(),
    )
    output = facade._get_onlinesales_request_context(
        page_type=SearchPageType.SEARCH, preview_mode=preview_mode
    )

    assert isinstance(output, CircuitBreaker)
    assert output.signature == expected_signature


@pytest.fixture
def os_products_response():
    """
    OS Response with 1 duplicate
    """
    return [
        {
            "uclid": "uclid-1001",
            "plid": 1001,
            "tsin": 2001,
            "sku_id": 3001,
            "seller_id": "M1234",
        },
        {
            "uclid": "uclid-1001",
            "plid": 1001,
            "tsin": 2001,
            "sku_id": 3001,
            "seller_id": "M1234",
        },
        {
            "uclid": "uclid-1002",
            "plid": 1002,
            "tsin": 2002,
            "sku_id": 3002,
            "seller_id": "M1234",
        },
        {
            "uclid": "uclid-1003",
            "plid": 1003,
            "tsin": 2003,
            "seller_id": "M1234",
        },
    ]


@pytest.fixture
def onlinesales_ads_response_products():
    return [
        {
            "sku_id": "201239357",
            "item_group_id": "90462193",
            "plid": "90462193",
            "seller_id": "M785811",
            "tsin": "90545828",
            "uclid": "2|rtmi8mxcjw1td2q25qmsi2h1w1zwihkp|0.095324995",
        },
        {
            "sku_id": "202118689",
            "item_group_id": "91098103",
            "plid": "91098103",
            "seller_id": "M29837126",
            "tsin": "91233115",
            "uclid": "2|75iy1de694oswtjxcs26fjn5cw89f2f5|0.095324995",
        },
        {
            "sku_id": "20211868911",
            "item_group_id": "91098103",
            "plid": "91098103",
            "seller_id": "M2983712611",
            "tsin": "9123311511",
            "uclid": "2|75iy1de694oswtjxcs26fjn5cw89f2f5|0.09532499511",
        },
        {
            # An item with missing fields that gets dropped early
            "uclid": "uclid-4",
            "sku_id": "98761",
            "seller_id": "M0981",
        },
    ]


@pytest.fixture
def onlinesales_ads_response_product_elements(onlinesales_ads_response_products):
    return {
        "ad_type": "product",
        "product_list": onlinesales_ads_response_products,
    }


@pytest.fixture
def onlinesales_ads_response_display_ad_elements():
    return {
        "ad_type": "banner",
        "landing_product_list": [
            {
                "sku_id": "93651156",
                "seller_id": "R11434",
                "tsin": "69311566",
                "plid": "72579690",
            },
            {
                # An item with missing fields that gets dropped early
                "uclid": "uclid-4",
                "sku_id": "98761",
                "seller_id": "M0981",
            },
        ],
        "bg_img_src_300x250": "https://www.test.com/img?300x250",
        "bg_img_src_300x50": "https://www.test.com/img?300x50",
        "bg_img_src_728x90": "https://www.test.com/img?728x90",
        "bg_img_src_1292x120": "https://www.test.com/img?1292x120",
    }


@pytest.fixture
def onlinesales_ads_response(
    onlinesales_ads_response_product_elements,
    onlinesales_ads_response_display_ad_elements,
):
    return {
        "ads": {
            "search-top": [
                {
                    "client_id": 198501,
                    "au": "search-top",
                    "uclid": "1|12345|12345",
                    "crt": "single-product",
                    "elements": onlinesales_ads_response_product_elements,
                }
            ],
            "pdp-slot-1": [
                {
                    "client_id": 198501,
                    "au": "pdp-slot-1",
                    "uclid": "2|67890|67890",
                    "crt": "single-product",
                    "elements": onlinesales_ads_response_display_ad_elements,
                }
            ],
        }
    }


@pytest.fixture
def products_request():
    return ProductsRequest(
        cli_ubid="cli_ubid",
        device=Device.DESKTOP,
        pcnt=20,
        page_type=SearchPageType.SEARCH,
        client_id="client_id",
        a_slot="a_slot",
    )


def test_get_products(
    mocker,
    mock_statsd,
    products_request,
    os_products_response,
    mock_config,
    mock_stats_client,
    mock_clients,
    mock_display_client,
    mock_products_client,
):
    facade = OnlinesalesFacade(
        config=mock_config,
        stats_client=mock_stats_client,
        display_client=mock_display_client,
        products_client=mock_products_client,
        response_factory=ResponseFactory(
            config=mock_config,
            destination_url_factory=mocker.Mock(),
        ),
    )

    facade._products_client.get_products_ads.return_value = {"products": os_products_response}
    output = facade.get_sponsored_products(request=products_request)
    facade._products_client.get_products_ads.assert_called_with(products_request)
    expected = ProductAdsResponse(
        products=[
            ProductAd(
                productline_id=1001,
                variant_id=2001,
                offer_id=3001,
                tracking_info=TrackingInfo(
                    uclid="uclid-1001", uuid=None, cli_ubid="cli_ubid", seller_id="M1234"
                ),
            ),
            ProductAd(
                productline_id=1002,
                variant_id=2002,
                offer_id=3002,
                tracking_info=TrackingInfo(
                    uclid="uclid-1002", uuid=None, cli_ubid="cli_ubid", seller_id="M1234"
                ),
            ),
        ]
    )

    assert output == expected


@pytest.fixture
def display_ads_request():
    return DisplayRequest(
        client_id="client_id",
        device_id="12345",
        ad_units=["search-top", "pdp-slot-1"],
        page_type=DisplayAdPageType.CATEGORY,
        device=Device.DESKTOP,
        filters={FilterKey.BRAND: ["Apple"]},
    )


@pytest.fixture
def display_ads_request_preview():
    return DisplayRequest(
        client_id="client_id",
        device_id="12345",
        ad_units=["search-top", "pdp-slot-1"],
        page_type=DisplayAdPageType.CATEGORY,
        device=Device.DESKTOP,
        filters={FilterKey.BRAND: ["Apple"]},
        preview_campaign_id="addles",
    )


@pytest.fixture
def display_ads_response():
    return DisplayAdsResponse(
        display_ads=[
            DisplayAd(
                ad_unit="search-top",
                ad_format="single-product",
                creative=Creative.SINGLE_PRODUCT,
                tracking_info=TrackingInfo(
                    uclid="1|12345|12345", uuid="198501", cli_ubid="12345", seller_id=None
                ),
                value=SingleProduct(
                    product=ProductAd(
                        productline_id=90462193,
                        variant_id=90545828,
                        offer_id=201239357,
                        tracking_info=TrackingInfo(
                            uclid="2|rtmi8mxcjw1td2q25qmsi2h1w1zwihkp|0.095324995",
                            uuid=None,
                            cli_ubid="12345",
                            seller_id="M785811",
                        ),
                    ),
                    destination_url="destination_url",
                ),
            ),
            DisplayAd(
                ad_unit="pdp-slot-1",
                ad_format="single-product",
                creative=Creative.SINGLE_PRODUCT,
                tracking_info=TrackingInfo(
                    uclid="2|67890|67890", uuid="198501", cli_ubid="12345", seller_id=None
                ),
                value=SingleProduct(
                    product=ProductAd(
                        productline_id=72579690,
                        variant_id=69311566,
                        offer_id=93651156,
                        tracking_info=TrackingInfo(
                            uclid="", uuid=None, cli_ubid="12345", seller_id="R11434"
                        ),
                    ),
                    destination_url="destination_url",
                ),
            ),
        ]
    )


@pytest.mark.parametrize(
    ("input_request", "expected_stats_key"),
    [
        (lf("display_ads_request"), "fetch_display_ads"),
        (lf("display_ads_request_preview"), "fetch_display_ads_preview"),
    ],
)
def test_get_display_ads(
    mocker,
    mock_statsd,
    input_request,
    onlinesales_ads_response,
    mock_display_client,
    mock_products_client,
    display_ads_response,
    expected_stats_key,
):
    destination_url_factory = MagicMock()
    destination_url_factory.from_display_ad.return_value = "destination_url"
    facade = OnlinesalesFacade(
        config=mocker.MagicMock(),
        stats_client=mock_statsd,
        display_client=mock_display_client,
        products_client=mock_products_client,
        response_factory=ResponseFactory(
            config=mocker.MagicMock(),
            destination_url_factory=destination_url_factory,
        ),
    )

    facade._display_client.get_display_ads.return_value = onlinesales_ads_response
    output = facade.get_sponsored_display(request=input_request)

    facade._display_client.get_display_ads.assert_called_with(input_request)

    assert output == display_ads_response
    # Check at least one stat to make sure the preview mode had an effect
    mock_statsd.incr.assert_has_calls(
        [
            mocker.call(
                f"custom.onlinesales.{expected_stats_key}.category_page.ad_units_requested", 2
            ),
        ],
        any_order=True,
    )


def test_get_display_ads_exceptions(
    mocker,
    mock_statsd,
    display_ads_request,
    onlinesales_ads_response,
    mock_display_client,
    mock_products_client,
):
    facade = OnlinesalesFacade(
        config=mocker.MagicMock(),
        stats_client=mocker.MagicMock(),
        display_client=mock_display_client,
        products_client=mock_products_client,
        response_factory=ResponseFactory(
            config=mocker.MagicMock(),
            destination_url_factory=mocker.MagicMock(),
        ),
    )

    facade._display_client.get_display_ads.side_effect = TimeoutException("Timeout")

    with pytest.raises(DownstreamError, match="onlinesales"):
        facade.get_sponsored_display(request=display_ads_request)
    facade._display_client.get_display_ads.assert_called_with(display_ads_request)


def test_get_products_exceptions(
    mocker,
    mock_statsd,
    products_request,
    os_products_response,
    mock_config,
    mock_stats_client,
    mock_clients,
    mock_display_client,
    mock_products_client,
):
    facade = OnlinesalesFacade(
        config=mock_config,
        stats_client=mock_stats_client,
        display_client=mock_display_client,
        products_client=mock_products_client,
        response_factory=ResponseFactory(
            config=mock_config,
            destination_url_factory=mocker.MagicMock(),
        ),
    )
    facade._products_client.get_products_ads.side_effect = TimeoutException("Timeout")

    with pytest.raises(DownstreamError, match="onlinesales"):
        facade.get_sponsored_products(request=products_request)
