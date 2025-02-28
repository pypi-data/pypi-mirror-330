import logging

import pytest

from client.sponsored_ads_client.protobuf import sponsored_ads_service_pb2 as pb
from sponsored_ads_service.protobuf.sponsored_ads_service_pb2 import (
    Creative,
    FilterValues,
    Location,
    Platform,
    Targeting,
)


@pytest.fixture(autouse=True)
def persistent_client(mocker):
    from client.sponsored_ads_client import s4f_client as module

    return mocker.patch.object(module, "PersistentServiceClient")


def test_client_init(mocker, persistent_client):
    from client.sponsored_ads_client.s4f_client import (
        LOGGING_FORMAT,
        SponsoredAdsClient,
    )

    mock_log_config = mocker.patch.object(logging, "basicConfig")

    output = SponsoredAdsClient(
        endpoints=["127.0.0.1:8000"],
        send_timeout=3000,
        recv_timeout=3000,
        connections=3,
    )
    mock_log_config.assert_called_with(
        stream=mocker.ANY, level=logging.INFO, format=LOGGING_FORMAT
    )
    persistent_client.assert_called_with(
        protobuf=pb,
        service_name="sponsored-ads-service",
        endpoints=["127.0.0.1:8000"],
        send_timeout=3000,
        recv_timeout=3000,
        connections=3,
    )
    output.client = persistent_client.return_value


def test_get_sponsored_display_all_parameters(mocker):
    from client.sponsored_ads_client.s4f_client import SponsoredAdsClient

    c = SponsoredAdsClient(endpoints=["127.0.0.1:8000"])
    mock_call = mocker.patch.object(c.client, "send")

    output = c.get_sponsored_display(
        location="LOCATION_ORDERS",
        platform="PLATFORM_WEB",
        uuid="1234-5678",
        creatives=["CREATIVE_BANNER", "CREATIVE_UNSPECIFIED"],
        ad_units=["pdp-slot-1"],
        plids=[1234567890, 2345678901, 3456789012],
        filters={"Brand": ["Sony", "Canon"], "Price": ["3000-*"]},
        timeout=3000,
    )

    mock_call.assert_called_with(
        pb.DisplayAdsRequest(
            location=Location.LOCATION_ORDERS,
            platform=Platform.PLATFORM_WEB,
            uuid="1234-5678",
            creatives=[Creative.CREATIVE_BANNER, Creative.CREATIVE_UNSPECIFIED],
            ad_units=["pdp-slot-1"],
            targeting=Targeting(
                plids=[1234567890, 2345678901, 3456789012],
                filters={
                    "Brand": FilterValues(values=["Sony", "Canon"]),
                    "Price": FilterValues(values=["3000-*"]),
                },
            ),
        ),
        version=c.version,
        timeout=3000,
    )
    assert output == mock_call.return_value


def test_get_sponsored_display_minimum_parameters(mocker):
    from client.sponsored_ads_client.s4f_client import SponsoredAdsClient

    c = SponsoredAdsClient(endpoints=["127.0.0.1:8000"])
    mock_call = mocker.patch.object(c.client, "send")

    output = c.get_sponsored_display(
        location="LOCATION_ORDERS",
        platform="PLATFORM_WEB",
        uuid="1234-5678",
        creatives=["CREATIVE_BANNER"],
        ad_units=["pdp-slot-1"],
    )

    mock_call.assert_called_with(
        pb.DisplayAdsRequest(
            location=Location.LOCATION_ORDERS,
            platform=Platform.PLATFORM_WEB,
            uuid="1234-5678",
            creatives=[Creative.CREATIVE_BANNER],
            ad_units=["pdp-slot-1"],
            targeting=Targeting(
                plids=[],
                filters={},
            ),
        ),
        version=c.version,
        timeout=None,
    )
    assert output == mock_call.return_value


def test_get_sponsored_products_minimum_parameters(mocker):
    from client.sponsored_ads_client.s4f_client import SponsoredAdsClient

    c = SponsoredAdsClient(endpoints=["127.0.0.1:8000"])
    mock_call = mocker.patch.object(c.client, "send")

    output = c.get_sponsored_products(
        location="LOCATION_ORDERS",
        platform="PLATFORM_WEB",
        uuid="1234-5678",
    )

    mock_call.assert_called_with(
        pb.ProductAdsRequest(
            location=Location.LOCATION_ORDERS,
            platform=Platform.PLATFORM_WEB,
            uuid="1234-5678",
            targeting=Targeting(
                plids=[],
                filters={},
            ),
        ),
        version=c.version,
        timeout=None,
    )
    assert output == mock_call.return_value


def test_get_sponsored_products_all_parameters(mocker):
    from client.sponsored_ads_client.s4f_client import SponsoredAdsClient

    c = SponsoredAdsClient(endpoints=["127.0.0.1:8000"])
    mock_call = mocker.patch.object(c.client, "send")

    output = c.get_sponsored_products(
        location="LOCATION_ORDERS",
        platform="PLATFORM_WEB",
        uuid="1234-5678",
        qsearch="test qsearch",
        filters={"Brand": ["Sony", "Canon"], "Price": ["3000-*"]},
        plids=[1234567890, 2345678901, 3456789012],
        cms_page_slug="slug",
        limit=10,
        timeout=3000,
    )

    mock_call.assert_called_with(
        pb.ProductAdsRequest(
            location=Location.LOCATION_ORDERS,
            platform=Platform.PLATFORM_WEB,
            uuid="1234-5678",
            targeting=Targeting(
                qsearch="test qsearch",
                filters={
                    "Brand": FilterValues(values=["Sony", "Canon"]),
                    "Price": FilterValues(values=["3000-*"]),
                },
                plids=[1234567890, 2345678901, 3456789012],
                cms_page_slug="slug",
            ),
            limit=10,
        ),
        version=c.version,
        timeout=3000,
    )
    assert output == mock_call.return_value


@pytest.mark.parametrize(
    ("filters", "expected"),
    [
        (None, []),
        ([], []),
        ([("Brand", ["Sony"])], [pb.Filter(name="Brand", values=["Sony"])]),
        (
            [("Brand", ["Sony", "Canon"]), ("Type", ["14"])],
            [
                pb.Filter(name="Brand", values=["Sony", "Canon"]),
                pb.Filter(name="Type", values=["14"]),
            ],
        ),
    ],
)
def test_parse_filter(filters, expected):
    from client.sponsored_ads_client.s4f_client import SponsoredAdsClient

    output = SponsoredAdsClient._parse_filters(filters)
    assert output == expected
