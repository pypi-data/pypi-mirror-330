from unittest.mock import MagicMock

import pytest

from sponsored_ads_service.onlinesales import CreativeFactory
from sponsored_ads_service.sponsored_ads.models import (
    Creative,
    DisplayAdsRequest,
    DisplayAdsResponse,
    Location,
    Platform,
    ProductAdsRequest,
    ProductAdsResponse,
    Targeting,
)


@pytest.fixture
def display_ads_request():
    return DisplayAdsRequest(
        location=Location.UNSPECIFIED,
        platform=Platform.UNSPECIFIED,
        uuid="uuid",
        creatives=[Creative.BANNER],
        ad_units=[],
        targeting=Targeting(
            qsearch="",
            filters={},
            plids=[],
            cms_page_slug="",
        ),
        limit=1,
        preview_campaign_id=None,
    )


@pytest.fixture
def product_ads_request():
    return ProductAdsRequest(
        location=Location.UNSPECIFIED,
        platform=Platform.UNSPECIFIED,
        uuid="uuid",
        targeting=Targeting(
            qsearch="",
            filters={},
            plids=[],
            cms_page_slug="",
        ),
        limit=1,
    )


@pytest.fixture
def mock_controller(mocker, config, mock_catalogue_aggregator_integration):
    from sponsored_ads_service.sponsored_ads.controller import SponsoredAdsController

    mock_hierarchy_factory = mocker.Mock()
    mock_hierarchy_factory.build_node_path.return_value = []

    controller = SponsoredAdsController()
    from sponsored_ads_service.onlinesales import RequestFactory

    controller._request_factory = RequestFactory(
        ad_slot_id="test-ad-slot-id",
        client_id="test-client-id",
        hierarchy_factory=mock_hierarchy_factory,
        onlinesales_creative_factory=CreativeFactory(config=config),
        stats_client=mocker.Mock(),
        catalogue_integration=mock_catalogue_aggregator_integration,
    )
    controller._request_factory.build_sponsored_display_request = MagicMock()
    controller._request_factory.build_products_request = MagicMock()
    controller._onlinesales_facade = MagicMock()
    controller._onlinesales_facade.get_sponsored_products = MagicMock()
    controller._onlinesales_facade.get_display_ads = MagicMock()
    controller._config.get_sponsored_products_plid_limit()

    return controller


@pytest.fixture
def product_ads_response():
    return ProductAdsResponse(products=[])


@pytest.fixture
def display_ads_response():
    return DisplayAdsResponse(display_ads=[])


def test_get_sponsored_display_no_ads(mock_controller, display_ads_request, display_ads_response):
    from sponsored_ads_service.onlinesales.models import ProductsRequest

    mock_controller._request_factory.build_sponsored_display_request.return_value = MagicMock(
        spec=ProductsRequest
    )
    mock_controller.get_sponsored_display(display_ads_request)
    mock_controller._onlinesales_facade.get_sponsored_display.assert_called_once()


def test_get_sponsored_products_no_ads(mock_controller, product_ads_request, product_ads_response):
    mock_controller._request_factory.build_products_request.return_value = MagicMock(
        spec=DisplayAdsResponse
    )
    mock_controller.get_sponsored_products(product_ads_request)
    mock_controller._onlinesales_facade.get_sponsored_products.assert_called_once()
