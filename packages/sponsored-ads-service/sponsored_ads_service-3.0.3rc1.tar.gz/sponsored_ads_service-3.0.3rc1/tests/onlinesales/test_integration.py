import os
from unittest.mock import MagicMock, patch

import pytest
from requests import Response
from requests.exceptions import JSONDecodeError
from rest_clients.exceptions import (
    DuplicateConstraintViolationException,
    InvalidServiceResponseException,
    ResourceNotFoundException,
    ValidationErrorException,
)

from sponsored_ads_service.onlinesales import DisplayClient, ProductsClient
from sponsored_ads_service.onlinesales.models import (
    Creative,
    Device,
    DisplayAdPageType,
    DisplayRequest,
    FilterKey,
    ProductsRequest,
    SearchPageType,
)


@pytest.fixture(autouse=True, scope="session")
def role_env(session_mocker):
    session_mocker.patch.dict(os.environ, {"ROLE": "test"})


@pytest.fixture
def os_products_response():
    return [
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


def test_get_products(mocker, mock_statsd, os_products_response):
    from sponsored_ads_service.onlinesales.integration import ProductsClient

    client = ProductsClient(
        config=mocker.MagicMock(),
    )
    mock_call = mocker.patch.object(
        client,
        "get",
        return_value={"products": os_products_response},
    )
    request = mocker.MagicMock(ProductsRequest)
    request.pcnt = 2
    request.page_type = SearchPageType.CUSTOM

    client.get_products_ads(request=request)
    mock_call.assert_called_with(
        resource_path="/sda",
        params=request.to_request_params(),
        operation_name="get_products_ads",
    )


def test_get_display_ads(mocker, mock_statsd, onlinesales_ads_response):
    from sponsored_ads_service.onlinesales.integration import DisplayClient

    client = DisplayClient(
        config=mocker.MagicMock(),
    )
    mock_call = mocker.patch.object(
        client,
        "get",
        return_value=onlinesales_ads_response,
    )
    request = mocker.MagicMock(DisplayRequest)
    request.ad_units = mocker.MagicMock()
    request.page_type = DisplayAdPageType.HOME
    request.preview_campaign_id = None

    client.get_display_ads(request=request)

    mock_call.assert_called_with(
        operation_name="get_display_ads",
        resource_path="/v2/bsda",
        params=request.to_request_params(),
    )


def test_get_display_ads_preview(mocker, mock_statsd, onlinesales_ads_response):
    from sponsored_ads_service.onlinesales.integration import DisplayClient

    client = DisplayClient(
        config=mocker.MagicMock(),
    )
    mock_call = mocker.patch.object(
        client,
        "get",
        return_value=onlinesales_ads_response,
    )
    request = mocker.MagicMock(DisplayRequest)
    request.ad_units = mocker.MagicMock()
    request.page_type = DisplayAdPageType.HOME
    request.preview_campaign_id = "show-me-the-ad"

    client.get_display_ads(request=request)

    mock_call.assert_called_with(
        operation_name="get_display_ads",
        resource_path="/preview/bsda",
        params=request.to_request_params(),
    )


@pytest.mark.parametrize(
    ("status_code", "exception"),
    [
        (400, ValidationErrorException),
        (404, ResourceNotFoundException),
        (409, DuplicateConstraintViolationException),
        (500, InvalidServiceResponseException),
    ],
)
def test_decode_response(status_code, exception, mock_statsd):
    from sponsored_ads_service.onlinesales.integration import _BaseOnlineSalesClient

    base_online_sales_client = _BaseOnlineSalesClient(config=MagicMock(), host="test-host")
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = status_code
    mock_response.json.return_value = {"error": {"message": "error message"}}
    with pytest.raises(exception):
        base_online_sales_client.decode_response(mock_response)


def test_decode_response_raises_for_invalid_json(mock_statsd):
    from sponsored_ads_service.onlinesales.integration import _BaseOnlineSalesClient

    base_online_sales_client = _BaseOnlineSalesClient(config=MagicMock(), host="test-host")
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.side_effect = JSONDecodeError("error", "doc", 0)

    with pytest.raises(InvalidServiceResponseException):
        base_online_sales_client.decode_response(mock_response)


def test_decode_response_valid_response(mocker, mock_statsd):
    from sponsored_ads_service.onlinesales.integration import _BaseOnlineSalesClient

    base_online_sales_client = _BaseOnlineSalesClient(config=MagicMock(), host="test-host")
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.json = mocker.Mock(return_value={"data": "test"})

    output = base_online_sales_client.decode_response(mock_response)
    assert output == {"data": "test"}


def test_decode_response_empty_response(mocker, mock_statsd):
    from sponsored_ads_service.onlinesales.integration import _BaseOnlineSalesClient

    base_online_sales_client = _BaseOnlineSalesClient(config=MagicMock(), host="test-host")
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.json = mocker.Mock(return_value=None)

    with pytest.raises(InvalidServiceResponseException):
        base_online_sales_client.decode_response(mock_response)


@pytest.fixture
def display_request():
    return DisplayRequest(
        client_id="client_id",
        device_id="device_id",
        device=Device.DESKTOP,
        ad_units=["ad_unit_1", "ad_unit_2"],
        page_type=DisplayAdPageType.HOME,
        creatives=[Creative.SINGLE_PRODUCT],
        filters={FilterKey.BRAND: ["Samsung", "Apple"], FilterKey.KEYWORD: ["mobile"]},
        preview_campaign_id=None,
    )


def test_successful_display_ad_request(display_request):
    display_client = DisplayClient(
        config=MagicMock(),
    )
    display_client.get = MagicMock(
        return_value={"ads": {"ad_unit_1": [{"elements": {"ad_type": "banner"}}]}}
    )
    with patch("random.uniform", return_value=0.5):
        response = display_client.get_display_ads(display_request)
        assert response == {"ads": {"ad_unit_1": [{"elements": {"ad_type": "banner"}}]}}
        display_client.get.assert_called_with(
            resource_path="/v2/bsda",
            params=display_request.to_request_params(),
            operation_name="get_display_ads",
        )


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


def test_successful_product_ad_request(products_request):
    products_client = ProductsClient(
        config=MagicMock(),
    )
    products_client.get = MagicMock(
        return_value={"ads": {"ad_unit_1": [{"elements": {"ad_type": "banner"}}]}}
    )
    with patch("random.uniform", return_value=0.5):
        response = products_client.get_products_ads(products_request)
        assert response == {"ads": {"ad_unit_1": [{"elements": {"ad_type": "banner"}}]}}
        products_client.get.assert_called_with(
            resource_path="/sda",
            params=products_request.to_request_params(),
            operation_name="get_products_ads",
        )
