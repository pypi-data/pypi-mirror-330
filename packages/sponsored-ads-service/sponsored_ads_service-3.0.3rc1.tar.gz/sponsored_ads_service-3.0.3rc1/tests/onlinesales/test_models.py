from unittest.mock import patch

import pytest

from sponsored_ads_service.onlinesales.models import (
    Creative,
    Device,
    DisplayAdPageType,
    DisplayRequest,
    FilterKey,
    ProductsRequest,
    SearchPageType,
)
from sponsored_ads_service.sponsored_ads import models as dto


@pytest.mark.parametrize(
    ("input_value", "expected_output"),
    [
        ("nonexistent", Creative.UNKNOWN),
        ("single-product", Creative.SINGLE_PRODUCT),
        ("", Creative.UNKNOWN),
        (None, Creative.UNKNOWN),
    ],
)
def test_missing_creative(input_value, expected_output):
    assert Creative(input_value) == expected_output


@pytest.mark.parametrize(
    (
        "device",
        "page_type",
        "expected_device",
        "expected_page_type",
    ),
    [
        (Device.ANDROID, SearchPageType.CATEGORY, "android", "CATEGORY"),
        (Device.DESKTOP, SearchPageType.HOME, "desktop", "HOME"),
        (Device.IOS, SearchPageType.PRODUCT, "ios", "PRODUCT"),
    ],
)
def test_products_request_to_request_params(
    device, page_type, expected_device, expected_page_type
):
    products_request = ProductsRequest(
        cli_ubid="test_cli_ubid",
        device=device,
        pcnt=1,
        page_type=page_type,
        client_id="test_client_id",
        a_slot="test_a_slot",
    )
    request_params = products_request.to_request_params()

    assert request_params["device"] == expected_device
    assert request_params["page_type"] == expected_page_type
    assert request_params["cli_ubid"] == "test_cli_ubid"
    assert request_params["pcnt"] == 1
    assert request_params["client_id"] == "test_client_id"
    assert request_params["a_slot"] == "test_a_slot"


@pytest.mark.parametrize(
    (
        "keywords",
        "brands",
        "categories",
        "sku_ids",
        "expected_keywords",
        "expected_brands",
        "expected_categories",
        "expected_sku_ids",
    ),
    [
        (
            ["keyword1", "keyword2"],
            ["brand1", "brand2"],
            ["category1", "category2"],
            [1, 2],
            ["keyword1", "keyword2"],
            ["brand1", "brand2"],
            ["category1", "category2"],
            [1, 2],
        ),
        (None, None, None, None, None, None, None, None),
    ],
)
def test_products_request_to_request_params_with_optional_fields(
    keywords,
    brands,
    categories,
    sku_ids,
    expected_keywords,
    expected_brands,
    expected_categories,
    expected_sku_ids,
):
    products_request = ProductsRequest(
        cli_ubid="test_cli_ubid",
        device=Device.ANDROID,
        pcnt=1,
        page_type=SearchPageType.CATEGORY,
        client_id="test_client_id",
        a_slot="test_a_slot",
        keywords=keywords,
        brands=brands,
        categories=categories,
        sku_ids=sku_ids,
    )
    request_params = products_request.to_request_params()

    assert request_params.get("keywords[]") == expected_keywords
    assert request_params.get("brands[]") == expected_brands
    assert request_params.get("categories[]") == expected_categories
    assert request_params.get("sku_ids[]") == expected_sku_ids


@pytest.mark.parametrize(
    ("location", "expected_page_type"),
    [
        (dto.Location.PDP, DisplayAdPageType.PDP),
        (dto.Location.SEARCH, DisplayAdPageType.SEARCH),
        (dto.Location.HOME, DisplayAdPageType.HOME),
        (dto.Location.LANDING_PAGE, DisplayAdPageType.CATEGORY),
        (dto.Location.ORDERS, DisplayAdPageType.ORDERS),
        (dto.Location.ORDER_DETAILS, DisplayAdPageType.ORDER_DETAILS),
        (dto.Location.ORDER_TRACKING, DisplayAdPageType.ORDER_TRACKING),
        (dto.Location.ORDER_CONFIRMATION, DisplayAdPageType.ORDER_CONFIRMATION),
        (dto.Location.CART, DisplayAdPageType.CART),
    ],
)
def test_location_to_page_type_mapping(location, expected_page_type):
    assert DisplayAdPageType.from_location(location) == expected_page_type


def test_location_to_page_type_mapping_error():
    with pytest.raises(ValueError):  # noqa PT011
        DisplayAdPageType.from_location(dto.Location.UNSPECIFIED)


@pytest.mark.parametrize(
    ("platform", "expected_device"),
    [
        (dto.Platform.ANDROID, Device.ANDROID),
        (dto.Platform.WEB, Device.DESKTOP),
        (dto.Platform.IOS, Device.IOS),
        ("nonexistent", Device.DESKTOP),
    ],
)
def test_platform_to_device_mapping(platform, expected_device):
    assert Device.from_platform(platform) == expected_device


@pytest.mark.parametrize(
    ("ad_units", "creatives", "filters", "preview_campaign_id", "expected"),
    [
        (
            ["ad_unit1", "ad_unit2"],
            [Creative.SINGLE_PRODUCT, Creative.MULTI_PRODUCT_3],
            {FilterKey.BRAND: "brand1", FilterKey.CATEGORIES: ["category1", "category2"]},
            None,
            {
                "ad_type": "brand_ads",
                "client_id": "test_client_id",
                "device_id": "test_device_id",
                "pt": "PRODUCT_PAGE",
                "au[]": ["ad_unit1", "ad_unit2"],
                "crt[]": ["single-product", "Multi-product-3"],
                "rn": 0.5,
                "f.device": "android",
                "f.brand": "brand1",
                "f.category_l1": "category1",
                "f.category_l2": "category2",
            },
        ),
        (
            ["ad_unit1"],
            [Creative.SINGLE_PRODUCT],
            {FilterKey.BRAND: "brand1"},
            None,
            {
                "ad_type": "brand_ads",
                "client_id": "test_client_id",
                "device_id": "test_device_id",
                "pt": "PRODUCT_PAGE",
                "au[]": ["ad_unit1"],
                "crt[]": ["single-product"],
                "rn": 0.5,
                "f.device": "android",
                "f.brand": "brand1",
            },
        ),
        (
            [],
            [],
            {},
            None,
            {
                "ad_type": "brand_ads",
                "client_id": "test_client_id",
                "device_id": "test_device_id",
                "pt": "PRODUCT_PAGE",
                "rn": 0.5,
                "f.device": "android",
            },
        ),
        (
            ["ad_unit1", "ad_unit2"],
            [Creative.SINGLE_PRODUCT, Creative.MULTI_PRODUCT_3],
            {FilterKey.BRAND: "brand1", FilterKey.CATEGORIES: ["category1", "category2"]},
            "preview-id-123",
            {
                "ad_type": "brand_ads",
                "client_id": "test_client_id",
                "device_id": "test_device_id",
                "pt": "PRODUCT_PAGE",
                "au[]": ["ad_unit1", "ad_unit2"],
                "crt[]": ["single-product", "Multi-product-3"],
                "rn": 0.5,
                "f.device": "android",
                "f.brand": "brand1",
                "f.category_l1": "category1",
                "f.category_l2": "category2",
                "campaign_id": "preview-id-123",
            },
        ),
    ],
)
def test_display_request_to_request_params(
    ad_units, creatives, filters, preview_campaign_id, expected
):
    with patch("random.uniform", return_value=0.5):
        display_request = DisplayRequest(
            client_id="test_client_id",
            device_id="test_device_id",
            page_type=DisplayAdPageType.PDP,
            device=Device.ANDROID,
            ad_units=ad_units,
            creatives=creatives,
            filters=filters,
            preview_campaign_id=preview_campaign_id,
        )
        request_params = display_request.to_request_params()

    assert request_params == expected
