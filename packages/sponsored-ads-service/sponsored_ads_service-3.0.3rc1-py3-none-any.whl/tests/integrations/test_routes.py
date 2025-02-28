import pytest
import s4f.errors
from cms_navigation_client import navigation_service_pb2 as pb

from sponsored_ads_service.errors import DownstreamTimeoutError
from sponsored_ads_service.models.link_data import ActionType, Context, LinkData

pytestmark = pytest.mark.integrations


@pytest.mark.parametrize(
    ("link", "link_data_response_pb", "link_data_return"),
    [
        (
            "https://www.takealot.com/cameras",
            pb.LinkData(
                action="page",
                context="navigation",
                parameters='{"url": "https://www.takealot.com/cameras", \
                "urls":{ "desktop": "https://www.takealot.com/cameras", \
                "mobiweb": "https://www.takealot.com/cameras"}, \
                "slug": "cameras", \
                "revision": "null", "path": "cameras" }',
                seo_info_found=False,
            ),
            LinkData(
                action=ActionType.PAGE,
                context=Context.NAVIGATION,
                parameters={
                    "url": "https://www.takealot.com/cameras",
                    "urls": {
                        "desktop": "https://www.takealot.com/cameras",
                        "mobiweb": "https://www.takealot.com/cameras",
                    },
                    "slug": "cameras",
                    "revision": "null",
                    "path": "cameras",
                },
                seo_info_found=False,
            ),
        ),
        (
            "https://www.wikipedia.org",
            pb.LinkData(
                action="notfound",
                context="navigation",
                parameters='{"url": "https://www.wikipedia.org"}',
                seo_info_found=False,
            ),
            LinkData(
                action=ActionType.NOT_FOUND,
                context=Context.NAVIGATION,
                parameters={
                    "url": "https://www.wikipedia.org",
                },
                seo_info_found=False,
            ),
        ),
    ],
)
def test_get_link_data(mocker, link, link_data_response_pb, link_data_return):
    from sponsored_ads_service.integrations.route import RouteIntegration

    mock_cms_nav_client = mocker.Mock()
    integration = RouteIntegration(cms_nav_client=mock_cms_nav_client)
    mock_cms_nav_client.get_link_data.return_value = pb.LinkDataResponse(
        link_data=link_data_response_pb
    )
    output = integration.get_link_data(link)
    assert output == link_data_return


def test_get_category_by_id_raises_timeout_errors(mocker):
    from sponsored_ads_service.integrations.route import RouteIntegration

    mock_cms_nav_client = mocker.Mock()
    integration = RouteIntegration(cms_nav_client=mock_cms_nav_client)
    mock_cms_nav_client.get_link_data.side_effect = s4f.errors.TimeoutError("Test Timeout Error")
    with pytest.raises(DownstreamTimeoutError):
        integration.get_link_data("https://www.takealot.com/cameras")
