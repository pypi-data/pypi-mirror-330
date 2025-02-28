from unittest.mock import MagicMock

import pytest
from pytest_lazy_fixtures import lf

from sponsored_ads_service.errors import UnsupportedLocationError
from sponsored_ads_service.onlinesales.models import (
    Device,
    DisplayAdPageType,
    DisplayRequest,
    FilterKey,
    ProductsRequest,
    SearchPageType,
)
from sponsored_ads_service.onlinesales.request_factory import RequestFactory
from sponsored_ads_service.sponsored_ads.models import (
    Creative,
    DisplayAdsRequest,
    Location,
    Platform,
    ProductAdsRequest,
    Targeting,
)


@pytest.fixture
def mock_factory():
    return MagicMock()


@pytest.fixture
def mock_creative_factory():
    return MagicMock()


@pytest.fixture
def mock_catalogue_integration():
    return MagicMock()


@pytest.fixture
def mock_stats_client():
    return MagicMock()


@pytest.fixture
def mock_config():
    return MagicMock()


@pytest.fixture
def mock_hierarchy_factory():
    from sponsored_ads_service.factories.hierarchy import HierarchyFactory

    mock_hierarchy_factory = MagicMock(spec=HierarchyFactory)

    def side_effect(filters, **kwargs):
        # If there are category filters, return the stubbed node path, otherwise return empty
        if filters.get("category"):
            return ["category1", "category2"]
        return []

    mock_hierarchy_factory.build_node_path.side_effect = side_effect
    return mock_hierarchy_factory


@pytest.fixture
def mock_display_ads_request():
    return DisplayAdsRequest(
        uuid="test_uuid",
        platform=Platform.ANDROID,
        location=Location.PDP,
        ad_units=["ad_unit1", "ad_unit2"],
        creatives=[Creative.BANNER, Creative.SINGLE_PRODUCT],
        targeting=Targeting(
            qsearch="test_qsearch",
            filters={"brand": ["brand1", "brand2"], "category": ["category1", "category2"]},
            plids=[1, 2, 3],
            cms_page_slug="test/slug",
        ),
        limit=10,
        preview_campaign_id=None,
    )


@pytest.fixture
def mock_display_ads_request_preview():
    return DisplayAdsRequest(
        uuid="test_uuid",
        platform=Platform.ANDROID,
        location=Location.PDP,
        ad_units=["ad_unit1", "ad_unit2"],
        creatives=[Creative.BANNER, Creative.SINGLE_PRODUCT],
        targeting=Targeting(
            qsearch="test_qsearch",
            filters={"brand": ["brand1", "brand2"], "category": ["category1", "category2"]},
            plids=[1, 2, 3],
            cms_page_slug="test/slug",
        ),
        limit=10,
        preview_campaign_id="191919",
    )


@pytest.mark.parametrize(
    ("display_ads_request", "expected_preview_campaign_id"),
    [
        (lf("mock_display_ads_request"), None),
        (lf("mock_display_ads_request_preview"), "191919"),
    ],
)
def test_build_sponsored_display(
    mock_factory,
    mock_creative_factory,
    mock_catalogue_aggregator_integration,
    mock_stats_client,
    mock_config,
    display_ads_request,
    mock_api_client,
    mock_aggregator_client,
    filtered_lineage_doc,
    expected_preview_campaign_id,
):
    from sponsored_ads_service.onlinesales import RequestFactory

    factory = RequestFactory(
        client_id="test_client_id",
        ad_slot_id="test_ad_slot_id",
        hierarchy_factory=mock_factory,
        onlinesales_creative_factory=mock_creative_factory,
        stats_client=mock_stats_client,
        catalogue_integration=mock_catalogue_aggregator_integration,
    )

    result = factory.build_sponsored_display_request(display_ads_request)

    assert isinstance(result, DisplayRequest)
    assert result.client_id == "test_client_id"
    assert result.device_id == "test_uuid"
    assert result.page_type == DisplayAdPageType.PDP
    assert result.device == Device.ANDROID
    assert result.ad_units == ["ad_unit1", "ad_unit2"]
    assert result.filters == {
        FilterKey.KEYWORD: "test_qsearch",
        FilterKey.CATEGORIES: mock_factory.build_node_path.return_value,
    }
    assert result.creatives == mock_creative_factory.from_request_creatives.return_value
    assert result.preview_campaign_id == expected_preview_campaign_id


def test_build_product_ads_request(
    mocker,
    mock_factory,
    mock_creative_factory,
    mock_stats_client,
    mock_hierarchy_factory,
    mock_catalogue_aggregator_integration,
):
    request = ProductAdsRequest(
        platform=Platform.WEB,
        location=Location.SEARCH,
        uuid="1234-5678",
        targeting=Targeting(
            qsearch="test_qsearch",
            filters={"brand": ["brand1", "brand2"], "category": ["category1", "category2"]},
            plids=[1, 2, 3],
            cms_page_slug="test/slug",
        ),
        limit=10,
    )

    factory = RequestFactory(
        client_id="test-client-id",
        ad_slot_id="test-ad-slot",
        hierarchy_factory=mock_hierarchy_factory,
        onlinesales_creative_factory=mock_creative_factory,
        stats_client=mock_stats_client,
        catalogue_integration=mock_catalogue_aggregator_integration,
    )
    output = factory.build_products_request(request)
    assert output == ProductsRequest(
        cli_ubid="1234-5678",
        device=Device.DESKTOP,
        sku_ids=[1, 2, 3],
        pcnt=10,
        page_type=SearchPageType.SEARCH,
        client_id="test-client-id",
        a_slot="test-ad-slot",
        keywords=["test_qsearch"],
        brands=[],
        categories=["category1", "category2"],
        rtl_custom_label_0=[],
    )


@pytest.mark.parametrize(
    ("location", "targeting", "expected"),
    [
        (Location.PDP, Targeting(), SearchPageType.PRODUCT),
        (Location.DEALS, Targeting(), SearchPageType.CUSTOM),
        (Location.SEARCH, Targeting(), SearchPageType.HOME),
        (Location.SEARCH, Targeting(qsearch="test_qsearch"), SearchPageType.SEARCH),
        (
            Location.SEARCH,
            Targeting(filters={"category": ["category1", "category2"]}),
            SearchPageType.CATEGORY,
        ),
    ],
)
def test_build_product_ads_request_page_type(
    mocker,
    mock_factory,
    mock_creative_factory,
    mock_stats_client,
    mock_hierarchy_factory,
    mock_catalogue_aggregator_integration,
    location,
    targeting,
    expected,
):
    request = ProductAdsRequest(
        platform=Platform.WEB, location=location, uuid="1234-5678", targeting=targeting, limit=10
    )

    factory = RequestFactory(
        client_id="test-client-id",
        ad_slot_id="test-ad-slot",
        hierarchy_factory=mock_hierarchy_factory,
        onlinesales_creative_factory=mock_creative_factory,
        stats_client=mock_stats_client,
        catalogue_integration=mock_catalogue_aggregator_integration,
    )
    output = factory.build_products_request(request)
    assert output.page_type == expected


def test_build_product_ads_request_unsupported_location(
    mocker,
    mock_factory,
    mock_creative_factory,
    mock_stats_client,
    mock_hierarchy_factory,
    mock_catalogue_aggregator_integration,
):
    request = ProductAdsRequest(
        platform=Platform.WEB,
        location=Location.ORDERS,
        uuid="1234-5678",
        targeting=Targeting(),
        limit=10,
    )

    factory = RequestFactory(
        client_id="test-client-id",
        ad_slot_id="test-ad-slot",
        hierarchy_factory=mock_hierarchy_factory,
        onlinesales_creative_factory=mock_creative_factory,
        stats_client=mock_stats_client,
        catalogue_integration=mock_catalogue_aggregator_integration,
    )
    with pytest.raises(UnsupportedLocationError):
        factory.build_products_request(request)


@pytest.mark.parametrize(
    ("client_request", "categories", "expected"),
    [
        (
            Targeting(
                filters={"Type": ["2"], "Brand": ["Adidas", "Nike"]},
                plids=[1001, 1002, 1003],
                cms_page_slug="test/slug",
                qsearch="",
            ),
            ["Sport", "Running"],
            {
                FilterKey.CATEGORIES: ["Sport", "Running"],
                FilterKey.BRAND: "Adidas,Nike",
            },
        ),
        (
            Targeting(
                filters={},
                qsearch="Air Foam",
                plids=[],
                cms_page_slug="",
            ),
            [],
            {
                FilterKey.KEYWORD: "Air Foam",
            },
        ),
    ],
)
def test_get_targeting_filters_for_search(
    mocker,
    config,
    mock_factory,
    mock_creative_factory,
    client_request,
    mock_stats_client,
    categories,
    expected,
):
    mock_hierarchy_factory = mocker.Mock()
    mock_hierarchy_factory.build_node_path.return_value = categories
    factory = RequestFactory(
        client_id="test-client-id",
        ad_slot_id="test-ad-slot",
        hierarchy_factory=mock_hierarchy_factory,
        onlinesales_creative_factory=mock_creative_factory,
        catalogue_integration=mocker.Mock(),
        stats_client=mock_stats_client,
    )
    output = factory._get_filters_from_targeting(client_request)
    assert output == expected


@pytest.mark.parametrize(
    ("filters", "expected"),
    [
        ({}, (None, None)),
        ({"Price": ["100-200", "300-500"]}, (None, None)),
        ({"Price": ["100-200"]}, (100, 200)),
        ({"Price": ["100-*"]}, (100, None)),
        ({"Price": ["*-200"]}, (None, 200)),
        ({"Price": ["INVALID-200"]}, (None, None)),
    ],
)
def test_get_prices(filters, expected):
    from sponsored_ads_service.onlinesales import RequestFactory

    output = RequestFactory._get_prices(filters)
    assert output == expected


@pytest.fixture
def catalogue_integration(mocker):
    return mocker.Mock()


@pytest.fixture
def stats_client(mocker):
    return mocker.Mock()


@pytest.fixture
def request_factory(mocker, catalogue_integration, stats_client):
    from sponsored_ads_service.onlinesales.request_factory import RequestFactory

    return RequestFactory(
        client_id="test_client",
        ad_slot_id="test_slot",
        hierarchy_factory=mocker.Mock(),
        catalogue_integration=catalogue_integration,
        onlinesales_creative_factory=mocker.Mock(),
        stats_client=stats_client,
    )


def test_returns_empty_filters_for_no_plids(request_factory):
    result = request_factory._get_filters_from_plids([])
    assert result == {}


def test_returns_empty_filters_for_multiple_plids(request_factory):
    result = request_factory._get_filters_from_plids([1, 2])
    assert result == {}


def test_returns_empty_filters_for_invalid_plid(request_factory, catalogue_integration):
    catalogue_integration.get_filtered_productline_adapters.return_value = {}
    result = request_factory._get_filters_from_plids([1])
    assert result == {}


def test_increments_stat_for_do_not_promote(
    mocker, request_factory, catalogue_integration, stats_client, johnny_walker_productline_adapter
):
    johnny_walker_productline_adapter.get_attribute_raw_value = mocker.MagicMock(return_value=True)
    catalogue_integration.get_filtered_productline_adapters.return_value = {
        "1": johnny_walker_productline_adapter
    }
    result = request_factory._get_filters_from_plids([1])
    stats_client.incr.assert_called_with(
        "custom.sponsored_display.request.filtered.do_not_promote_other"
    )
    assert result == {}


def test_increments_stat_for_no_buyable_offers(
    mocker, request_factory, catalogue_integration, stats_client, johnny_walker_productline_adapter
):
    request_factory._get_offer_ids_from_productline = mocker.Mock(return_value=[])
    catalogue_integration.get_filtered_productline_adapters.return_value = {
        "1": johnny_walker_productline_adapter
    }
    result = request_factory._get_filters_from_plids([1])
    stats_client.incr.assert_called_with(
        "custom.sponsored_display.request.filtered.no_buyable_offers"
    )
    assert result == {}


def test_returns_correct_filters_for_valid_plid(
    mocker, request_factory, catalogue_integration, johnny_walker_productline_adapter
):
    catalogue_integration.get_filtered_productline_adapters.return_value = {
        "1": johnny_walker_productline_adapter
    }
    result = request_factory._get_filters_from_plids([1])
    assert result == {
        FilterKey.SKU: 53587715,
        FilterKey.BRAND: "Johnnie Walker",
        FilterKey.CATEGORIES: ["Home & Kitchen", "Liquor", "Whiskey, Gin & Spirits", "Whiskey"],
    }
