from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

import click
from s4f.queue_pipeline_server import QueuePipelineServer
from s4f.rpc_message_handler import RpcMessageHandler

from sponsored_ads_service.configuration import Clients, SponsoredAdsConfig
from sponsored_ads_service.protobuf import sponsored_ads_service_pb2 as pb
from sponsored_ads_service.sponsored_ads.controller import SponsoredAdsController
from sponsored_ads_service.sponsored_ads.models import (
    DisplayAdsRequest,
    ProductAdsRequest,
)

if TYPE_CHECKING:
    from s4f.compiled_protobuffs.header_pb2 import RequestHeader

logger = logging.getLogger(__name__)


class SponsoredAdsService:
    def __init__(self, config: SponsoredAdsConfig, clients: Clients) -> None:
        self.config = config
        self.clients = clients
        self.version = self.config.get_version()
        self.display_ads_controller = SponsoredAdsController()

    def get_sponsored_display(
        self, request: pb.DisplayAdsRequest, header: RequestHeader
    ) -> pb.DisplayAdsResponse:
        """Get the sponsored display ads for a given product"""
        result = self.display_ads_controller.get_sponsored_display(
            request=DisplayAdsRequest.from_pb(request)
        )
        return result.to_pb()

    def get_sponsored_products(
        self, request: pb.ProductAdsRequest, header: RequestHeader
    ) -> pb.ProductAdsResponse:
        """Get the sponsored display ads for a given product"""
        result = self.display_ads_controller.get_sponsored_products(
            request=ProductAdsRequest.from_pb(request)
        )
        return result.to_pb()


def get_rpc_handler(
    service: SponsoredAdsService, config: SponsoredAdsConfig, clients: Clients
) -> RpcMessageHandler:
    handler = RpcMessageHandler(
        protobuf=pb,
        stats_client=clients.stats_client,
        service_version=service.version,
        sentry_config=config.get_sentry_settings(),
    )
    handler.route("DisplayAds")(service.get_sponsored_display)
    handler.route("ProductAds")(service.get_sponsored_products)

    return handler


@click.command()
@click.option("--port", default=9058, type=click.INT, help="Port to serve on.")
@click.option("--workers", default=5, type=click.INT, help="Number of workers to start.")
@click.option("--loglevel", default=logging.INFO, type=click.INT, help="Sets the level of logging")
def serve(port: int, workers: int, loglevel: int) -> None:
    log_format = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"
    logging.basicConfig(stream=sys.stdout, level=loglevel, format=log_format, force=True)
    logging.getLogger(__name__).info("Log level set to %d", loglevel)

    config = SponsoredAdsConfig()
    clients = Clients()
    service = SponsoredAdsService(config=config, clients=clients)
    handler = get_rpc_handler(service, config, clients)
    server = QueuePipelineServer(
        port=port, message_handler=handler, workers=workers, use_threads=False
    )
    server.serve()
