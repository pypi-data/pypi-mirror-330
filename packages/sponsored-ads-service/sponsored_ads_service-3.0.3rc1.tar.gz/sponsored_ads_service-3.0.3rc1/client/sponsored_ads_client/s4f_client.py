import logging
import sys
from typing import Optional

from s4f.persistent_client import PersistentServiceClient

from .protobuf import sponsored_ads_service_pb2 as pb

LOGGING_FORMAT = (
    "%(asctime)s %(levelname)s %(threadName)s %(filename)s:%(lineno)s %(message)s"
)

Filters = list[tuple[str, list[str]]]  # Helper type

_DEFAULT_VERSION = 1


class SponsoredAdsClient:
    """An S4F client responsible for making requests to the sponsored-ads-service"""

    service_name = "sponsored-ads-service"

    def __init__(
        self,
        endpoints: list[str],
        send_timeout: int = 1000,
        recv_timeout: int = 1000,
        connections: int = 5,
        version: Optional[int] = None,
    ) -> None:
        logging.basicConfig(
            stream=sys.stdout, level=logging.INFO, format=LOGGING_FORMAT
        )
        self.logger = logging.getLogger(__name__)
        self.version = version or _DEFAULT_VERSION
        self.client = PersistentServiceClient(
            protobuf=pb,
            service_name=self.service_name,
            endpoints=endpoints,
            send_timeout=send_timeout,
            recv_timeout=recv_timeout,
            connections=connections,
        )

    def get_sponsored_display(
        self,
        location: pb.Location,
        platform: pb.Platform,
        uuid: str,
        creatives: list[pb.Creative],
        ad_units: list[str],
        *,
        qsearch: Optional[str] = None,
        filters: Optional[dict[str, list[str]]] = None,
        plids: Optional[list[int]] = None,
        cms_page_slug: Optional[str] = None,
        limit: Optional[int] = None,
        preview_campaign_id: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> pb.DisplayAdsResponse:
        """Fetch sponsored display ads from Online Sales for product display pages"""
        request = pb.DisplayAdsRequest(
            location=location,
            uuid=uuid,
            platform=platform,
            creatives=creatives,
            ad_units=ad_units,
            targeting=pb.Targeting(
                qsearch=qsearch,
                filters=self._parse_filter_values(filters),
                plids=plids,
                cms_page_slug=cms_page_slug,
            ),
            limit=limit,
            preview_campaign_id=preview_campaign_id,
        )
        return self.client.send(request, version=self.version, timeout=timeout)

    def get_sponsored_products(
        self,
        location: pb.Location,
        platform: pb.Platform,
        uuid: str,
        *,
        qsearch: Optional[str] = None,
        filters: Optional[dict[str, list[str]]] = None,
        plids: Optional[list[int]] = None,
        cms_page_slug: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> pb.ProductAdsResponse:
        """Fetch sponsored display ads from Online Sales for product display pages"""
        request = pb.ProductAdsRequest(
            location=location,
            uuid=uuid,
            platform=platform,
            targeting=pb.Targeting(
                qsearch=qsearch,
                filters=self._parse_filter_values(filters),
                plids=plids,
                cms_page_slug=cms_page_slug,
            ),
            limit=limit,
        )
        return self.client.send(request, version=self.version, timeout=timeout)

    @staticmethod
    def _parse_filters(filters: Optional[Filters]) -> list[pb.Filter]:
        """
        A helper method for parsing the filters into a format understood by protobuffs
        """
        if filters:
            return [pb.Filter(name=name, values=values) for name, values in filters]
        return []

    @staticmethod
    def _parse_filter_values(
        filters: Optional[dict[str, list[str]]],
    ) -> dict[str, pb.FilterValues]:
        """
        A helper method for parsing the filters into a format understood by protobuffs
        """
        if filters:
            return {
                key: pb.FilterValues(values=values) for key, values in filters.items()
            }
        return {}
