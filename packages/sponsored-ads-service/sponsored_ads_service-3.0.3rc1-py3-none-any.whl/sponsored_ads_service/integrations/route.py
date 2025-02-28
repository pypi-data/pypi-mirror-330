import s4f.errors
from cms_navigation_client import CmsNavigationClient
from opentelemetry import trace

from sponsored_ads_service.errors import DownstreamTimeoutError
from sponsored_ads_service.models.link_data import LinkData
from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils
from sponsored_ads_service.utils.localcache import LocalcacheUtils

tracer = trace.get_tracer(__name__)


class RouteIntegration:
    def __init__(
        self,
        cms_nav_client: CmsNavigationClient,
    ) -> None:
        self._cms_nav_client = cms_nav_client

    @tracer.start_as_current_span("RoutesIntegration.get_link_data")
    @LocalcacheUtils.cached_from_config("routes_link_data")
    @MemcacheUtils.cached_from_config("routes_link_data")
    def get_link_data(self, link: str) -> LinkData:
        try:
            response = self._cms_nav_client.get_link_data(link=link)
        except (s4f.errors.TimeoutError, s4f.errors.CommunicationError):
            raise DownstreamTimeoutError("cms-navigation-service")

        return LinkData.from_pb(response.link_data)
