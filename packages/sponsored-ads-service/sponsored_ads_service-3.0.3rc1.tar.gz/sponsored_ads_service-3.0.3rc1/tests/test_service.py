import logging

import pytest
from click.testing import CliRunner
from s4f.compiled_protobuffs.header_pb2 import RequestHeader

from sponsored_ads_service.protobuf import sponsored_ads_service_pb2 as pb
from sponsored_ads_service.sponsored_ads.models import (
    DisplayAdsRequest,
    DisplayAdsResponse,
    Location,
    Platform,
    ProductAdsRequest,
    ProductAdsResponse,
    Targeting,
)
from tests.helpers import MockHandler

pytestmark = pytest.mark.service


def test_get_sponsored_display(mocker):
    from sponsored_ads_service.service import SponsoredAdsService

    service = SponsoredAdsService(config=mocker.Mock(), clients=mocker.Mock())
    response = DisplayAdsResponse()
    mock_call = mocker.patch.object(
        service.display_ads_controller,
        "get_sponsored_display",
        return_value=response,
    )
    output = service.get_sponsored_display(
        pb.DisplayAdsRequest(
            location=pb.Location.LOCATION_ORDERS,
            platform=pb.Platform.PLATFORM_ANDROID,
            uuid="1234",
            creatives=[],
            ad_units=[],
        ),
        RequestHeader(version=1),
    )
    mock_call.assert_called_with(
        request=DisplayAdsRequest(
            location=Location.ORDERS,
            platform=Platform.ANDROID,
            uuid="1234",
            creatives=[],
            ad_units=[],
            targeting=Targeting(
                qsearch="",
                filters={},
                plids=[],
                cms_page_slug="",
            ),
            limit=0,
            preview_campaign_id=None,
        )
    )
    assert output == response.to_pb()


def test_get_sponsored_products(mocker):
    from sponsored_ads_service.service import SponsoredAdsService

    service = SponsoredAdsService(config=mocker.Mock(), clients=mocker.Mock())
    response = ProductAdsResponse()
    mock_call = mocker.patch.object(
        service.display_ads_controller,
        "get_sponsored_products",
        return_value=response,
    )
    output = service.get_sponsored_products(
        pb.ProductAdsRequest(
            location=pb.Location.LOCATION_ORDERS,
            platform=pb.Platform.PLATFORM_ANDROID,
            uuid="1234",
            targeting=pb.Targeting(
                qsearch="",
                filters={},
                plids=[1, 2, 3, 4],
                cms_page_slug="",
            ),
            limit=5,
        ),
        RequestHeader(version=1),
    )
    mock_call.assert_called_with(
        request=ProductAdsRequest(
            location=Location.ORDERS,
            platform=Platform.ANDROID,
            uuid="1234",
            targeting=Targeting(
                qsearch="",
                filters={},
                plids=[1, 2, 3, 4],
                cms_page_slug="",
            ),
            limit=5,
        )
    )
    assert output == response.to_pb()


def test_get_rpc_handler(mocker):
    from sponsored_ads_service import service as module

    mock_service = mocker.Mock()
    mock_config = mocker.Mock()
    mock_clients = mocker.Mock()
    mock_handler = MockHandler()
    mock_handler_init = mocker.patch.object(module, "RpcMessageHandler", return_value=mock_handler)

    output = module.get_rpc_handler(mock_service, mock_config, mock_clients)

    mock_handler_init.assert_called_with(
        protobuf=pb,
        stats_client=mock_clients.stats_client,
        service_version=mock_service.version,
        sentry_config=mock_config.get_sentry_settings.return_value,
    )

    mock_handler.assert_has_only_routes(
        [
            ("DisplayAds", mock_service.get_sponsored_display),
            ("ProductAds", mock_service.get_sponsored_products),
        ]
    )
    assert output == mock_handler


@pytest.mark.parametrize(
    ("invoke_kwargs", "port", "workers", "loglevel"),
    [
        ([], 9058, 5, logging.INFO),
        (["--port", "8000"], 8000, 5, logging.INFO),
        (["--port", "3000", "--workers", "3", "--loglevel", "50"], 3000, 3, 50),
    ],
)
def test_serve(mocker, invoke_kwargs, port, workers, loglevel):
    from sponsored_ads_service import service as module

    mock_log_config = mocker.patch.object(module.logging, "basicConfig")
    mock_get_rpc_handler = mocker.patch.object(module, "get_rpc_handler")
    mock_init_server = mocker.patch.object(module, "QueuePipelineServer")

    runner = CliRunner()
    runner.invoke(module.serve, invoke_kwargs)

    mock_log_config.assert_called_with(
        stream=mocker.ANY,
        level=loglevel,
        format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
        force=True,
    )
    mock_init_server.assert_called_with(
        port=port,
        message_handler=mock_get_rpc_handler.return_value,
        workers=workers,
        use_threads=False,
    )
    mock_init_server.return_value.serve.assert_called_with()
