import json
import logging
import os
from collections.abc import Callable
from time import perf_counter
from typing import Any, TypeVar

import click
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message
from s4f.compiled_protobuffs.header_pb2 import RequestHeader
from s4f.errors import ServiceError
from s4f_clients.utils.protocolbuffer import dict_to_protocolbuffer

from sponsored_ads_service.configuration import Clients, SponsoredAdsConfig
from sponsored_ads_service.protobuf import sponsored_ads_service_pb2 as pb
from sponsored_ads_service.service import SponsoredAdsService, get_rpc_handler

# Module imports already caused the root logger to be initialised
# with a default level and format. To make this cli tool less
# verbose we need to take that level down here.
logging.getLogger().setLevel(logging.WARNING)

os.environ["STATSD_HOST_PORT"] = "127.0.0.1:8125"

config = SponsoredAdsConfig()
clients = Clients()
service = SponsoredAdsService(config=config, clients=clients)
handler = get_rpc_handler(service=service, config=config, clients=clients)


@click.group()
def cli() -> None: ...


_T = TypeVar("_T", bound=Message)

# Add custom formatters for certain responses
# In the form of Response PB Message -> formatter
_FORMATTERS: dict[Any, Callable[[dict], dict]] = {}


def _make_request(func: Callable[[_T, int], Message], request: _T, version: int) -> None:
    try:
        start = perf_counter()
        res = func(request, RequestHeader(version=version))
        end = perf_counter()
        diff = round((end - start) * 1000, 2)
        _display(res)
        click.echo(f"Call completed in {diff}ms")
    except ServiceError as se:
        click.echo("*** A service error was returned ***")
        click.echo(f"[{se.error_code}] {se}")


def _display(message: Message) -> None:
    """
    Pretty print the contents of a protocol buffer message.
    """
    message_as_dict: dict[str, Any] = MessageToDict(
        message,
        preserving_proto_field_name=True,
        use_integers_for_enums=False,  # This is only for display purposes
    )
    formatter = _FORMATTERS.get(type(message))
    if formatter:  # Check if there is a registered formatter for this response PB
        message_as_dict = formatter(message_as_dict)
    message_as_string = json.dumps(message_as_dict, indent=2)
    click.echo(message_as_string)


@cli.command()
def endpoints() -> None:
    """List all of the available protobuf requests (handlers)"""
    for route in handler.handlers:
        click.echo(route)


@cli.command()
@click.option(
    "--proto",
    type=click.STRING,
    prompt="Enter a request protobuf name",
    help="The name of the request protobuf to use",
)
@click.option(
    "--params",
    type=click.STRING,
    prompt="Enter the request parameters (as json)",
    help="The request parameters (as json)",
    default={},
)
@click.option(
    "--version",
    type=click.INT,
    help="The API version to use",
    default=1,
)
def endpoint(proto: str, params: str, version: int) -> None:
    """Make a request based on the given protobuf name and data"""
    proto = f"{proto}Request" if not proto.endswith("Request") else proto
    request_proto = getattr(pb, proto, None)
    if not request_proto:
        raise click.exceptions.BadParameter(
            f"Protobuf message {proto} does not exist",
            param_hint="proto",
        )
    request = request_proto()
    if params:
        dict_to_protocolbuffer(json.loads(params), request)
    req_route = handler.handlers.get(proto[:-7])
    if not req_route:
        raise click.exceptions.ClickException(f"RPC handler has no route for {proto[:-7]}")
    _make_request(req_route, request, version)


if __name__ == "__main__":
    cli()
