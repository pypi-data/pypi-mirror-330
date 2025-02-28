from functools import wraps

import pytest
from tal_stats_client import StatsClient

from sponsored_ads_service.models.hierarchy import Category, Department
from sponsored_ads_service.models.onlinesales import (
    OnlineSalesCreative,
    OnlineSalesDisplay,
    OnlineSalesProduct,
)
from sponsored_ads_service.models.sponsored_display import (
    AdType,
    Breakpoint,
    SponsoredDisplay,
    SponsoredDisplayCreative,
)
from sponsored_ads_service.models.sponsored_product import (
    OnlineSalesAdInfo,
    SponsoredProduct,
)


@pytest.fixture
def mock_decorator():
    def decorator(*args, **kwargs):
        def wrapped(f):
            @wraps(f)
            def inner(*args, **kwargs):
                return f(*args, **kwargs)

            return inner

        return wrapped

    return decorator


@pytest.fixture(autouse=True)
def config(mocker):
    mock_config = mocker.patch("sponsored_ads_service.configuration.SponsoredAdsConfig", spec=True)
    mocker.patch.object(mock_config, "get_rollout_flag_search_banner_remap", return_value=True)
    return mock_config


@pytest.fixture
def mock_statsd(mocker):
    m = mocker.MagicMock()
    mocker.patch("statsd.StatsClient", autospec=True, return_value=m)
    return m


@pytest.fixture(autouse=True)
def mock_tal_stats(mock_statsd):
    """For consistency, we need to reset the stats client before each test"""
    StatsClient._instance = None

    stats_client = StatsClient()
    stats_client.configure("127.0.0.1", 8125, False)

    return stats_client


@pytest.fixture(autouse=True)
def singleton(mocker):
    from sponsored_ads_service.utils.singleton import SingletonMeta

    def dummy_call(cls, *args, **kwargs):
        return type.__call__(cls, *args, **kwargs)

    mocker.patch.object(SingletonMeta, "__call__", dummy_call)


@pytest.fixture(autouse=True)
def sponsored_products_client_id(config):
    client_id = "client-id"
    config().get_sponsored_products_client_id.return_value = client_id
    return client_id


@pytest.fixture(autouse=True)
def sponsored_display_client_id(config):
    client_id = "client-id"
    config().get_sponsored_display_client_id.return_value = client_id
    return client_id


@pytest.fixture(autouse=True)
def sponsored_display_search_filters_plid_limit(config):
    plid_limit = 32
    config().get_sponsored_display_search_filters_plid_limit.return_value = plid_limit
    return plid_limit


@pytest.fixture(autouse=True)
def link_data_hostname(config):
    hostname = "www.abc.xyz"
    config().get_link_data_hostname.return_value = hostname
    return hostname


@pytest.fixture(autouse=True)
def clients(mocker):
    return mocker.patch("sponsored_ads_service.configuration.Clients")


@pytest.fixture(autouse=True)
def localcache_utils(mocker, mock_decorator):
    mock = mocker.patch("sponsored_ads_service.utils.localcache.LocalcacheUtils")
    mock.cached = mock_decorator
    mock.cached_from_config = mock_decorator
    return mock


@pytest.fixture(autouse=True)
def memcache_utils(mocker, mock_decorator):
    mock = mocker.patch("sponsored_ads_service.utils.legacy.memcache.MemcacheUtils")
    mock.cached = mock_decorator
    mock.cached_from_config = mock_decorator
    return mock


@pytest.fixture
def gaming():
    return Department(id=2, name="Gaming", slug="gaming")


@pytest.fixture
def books():
    return Department(id=3, name="Books", slug="books")


@pytest.fixture
def academic():
    return Category(
        id=15662,
        name="Academic",
        department_id=3,
        slug="academic-15662",
        parent_id=None,
    )


@pytest.fixture
def unisa():
    return Category(id=20176, name="Unisa", slug="unisa-20176", department_id=3, parent_id=15662)


@pytest.fixture
def sponsored_product_1001():
    return SponsoredProduct(
        lineage_document={"productline": {"id": 1001}},
        sponsored_ad=OnlineSalesAdInfo(
            text_notices=[],
            image_notices=[],
            uclid="uclid-1001",
            client_id="1234",
            cli_ubid="1234-5678",
            seller_id="M1234",
        ),
    )


@pytest.fixture
def sponsored_product_1002():
    return SponsoredProduct(
        lineage_document={"productline": {"id": 1002}},
        sponsored_ad=OnlineSalesAdInfo(
            text_notices=[],
            image_notices=[],
            uclid="uclid-1002",
            client_id="1234",
            cli_ubid="1234-5678",
            seller_id="M1234",
        ),
    )


@pytest.fixture
def sponsored_product_1003():
    return SponsoredProduct(
        lineage_document={"productline": {"id": 1003}},
        sponsored_ad=OnlineSalesAdInfo(
            text_notices=[],
            image_notices=[],
            uclid="uclid-1003",
            client_id="1234",
            cli_ubid="1234-5678",
            seller_id="M1234",
        ),
    )


@pytest.fixture
def sponsored_products(sponsored_product_1001, sponsored_product_1002, sponsored_product_1003):
    return [sponsored_product_1001, sponsored_product_1002, sponsored_product_1003]


@pytest.fixture
def filtered_lineage_doc():
    return {
        "productline": {
            "id": 123456,
            "hierarchies": {
                "business": {
                    "lineages": [
                        [
                            {
                                "id": 15017,
                                "name": "Uninterrupted Power Supply (UPS)",
                                "slug": "uninterrupted-power-supply-ups--15017",
                                "parent_id": 15012,
                                "forest_id": None,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.4},
                            },
                            {
                                "id": 15012,
                                "name": "Smart Energy Solutions",
                                "slug": "smart-energy-solutions-15012",
                                "parent_id": 14526,
                                "forest_id": None,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.4},
                            },
                            {
                                "id": 14526,
                                "name": "DIY & Automotive",
                                "slug": "diy-automotive-14526",
                                "parent_id": None,
                                "forest_id": 3,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.3},
                            },
                        ]
                    ],
                    "forests": [{"id": 3, "name": "Home", "slug": None}],
                },
                "taxonomy": {
                    "lineages": [
                        [
                            {
                                "id": 22306,
                                "name": "Uninterrupted Power Supply (UPS)",
                                "slug": "uninterrupted-power-supply-ups--22306",
                                "parent_id": 21508,
                                "forest_id": None,
                                "metadata": {},
                            },
                            {
                                "id": 21508,
                                "name": "Smart Energy Solutions",
                                "slug": "smart-energy-solutions-21508",
                                "parent_id": 15397,
                                "forest_id": None,
                                "metadata": {},
                            },
                            {
                                "id": 15397,
                                "name": "*Electronics",
                                "slug": "electronics-15397",
                                "parent_id": None,
                                "forest_id": 7,
                                "metadata": {"department": 4, "google_taxonomy": 222},
                            },
                        ]
                    ],
                    "forests": [{"id": 7, "name": "google", "slug": None}],
                },
                "merchandising": {
                    "lineages": [
                        [
                            {
                                "id": 27220,
                                "name": "Smart Home & Connected Living",
                                "slug": "smart-home-and-connected-living-27220",
                                "forest_id": 13,
                                "parent_id": None,
                                "metadata": {},
                            },
                            {
                                "id": 27245,
                                "name": "Smart Energy Solutions",
                                "slug": "smart-energy-solutions-27245",
                                "forest_id": None,
                                "parent_id": 27220,
                                "metadata": {},
                            },
                            {
                                "id": 27250,
                                "name": "Uninterrupted Power Supply (UPS)",
                                "slug": "uninterrupted-power-supply-ups-27250",
                                "forest_id": None,
                                "parent_id": 27245,
                                "metadata": {},
                            },
                        ]
                    ],
                    "forests": [{"id": 13, "name": "Computers & Tablets", "slug": "computers"}],
                },
            },
            "attributes": {
                "brand": {
                    "display_name": "Brand",
                    "display_value": "RCT",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "id": 1605,
                        "name": "RCT",
                        "object": {
                            "image_url": "https://media.takealot.com/brands/rct.gif",
                            "department_ids": [13, 16],
                        },
                        "sort_order": 1789100,
                    },
                },
            },
        },
        "variants": {
            "2101": {
                "variant": {"id": 2101, "availability": {"status": "buyable"}},
                "offers": {"3101": {"id": 3101, "availability": {"status": "buyable"}}},
            },
            "2102": {
                "variant": {"id": 2102, "availability": {"status": "buyable"}},
                "offers": {
                    "3201": {"id": 3201, "availability": {"status": "non_buyable"}},
                    "3202": {"id": 3202, "availability": {"status": "buyable"}},
                },
            },
            "2103": {
                "variant": {"id": 2103, "availability": {"status": "non_buyable"}},
                "offers": {"3301": {"id": 3301, "availability": {"status": "non_buyable"}}},
            },
        },
    }


@pytest.fixture
def mock_api_client(mocker):
    from catalogue_client.http_client import CatalogueHttpClient

    return mocker.Mock(spec=CatalogueHttpClient)


@pytest.fixture
def mock_aggregator_client(mocker):
    from catalogue_aggregator_client.http_client import CatalogueAggregatorHttpClient

    return mocker.Mock(spec=CatalogueAggregatorHttpClient)


@pytest.fixture
def sd_model_empty():
    return SponsoredDisplay(
        ad_type=AdType.PRODUCT,
        client_id="client-id",
        ad_unit="search-top",
        uclid="abc|123|",
        creative=SponsoredDisplayCreative.SINGLE_PRODUCT,
        destination_url="",
        products=[],
        background={},
    )


@pytest.fixture
def sd_model_products(sponsored_product_1001, sponsored_product_1003):
    return SponsoredDisplay(
        ad_type=AdType.PRODUCT,
        client_id="client-id",
        ad_unit="search-top",
        uclid="abc|123|",
        creative=SponsoredDisplayCreative.SINGLE_PRODUCT,
        destination_url="https://foo.bar/here?boo",
        products=[sponsored_product_1001, sponsored_product_1003],
        background={
            Breakpoint.SMALL: {"src": "https://aaa.bbb/img?sz=s", "width": 101, "height": 100},
            Breakpoint.MEDIUM: {"src": "https://aaa.bbb/img?sz=m", "width": 201, "height": 200},
            Breakpoint.LARGE: {"src": "https://aaa.bbb/img?sz=l", "width": 301, "height": 300},
        },
    )


@pytest.fixture
def sd_model_banner():
    return SponsoredDisplay(
        ad_type=AdType.BANNER,
        client_id="client-id",
        ad_unit="search-top",
        uclid="abc|123|",
        creative=SponsoredDisplayCreative.SEARCH_BANNER,
        destination_url="https://foo.bar/here?boo",
        products=[],
        background={
            Breakpoint.SMALL: {"src": "https://aaa.bbb/img?sz=s", "width": 103, "height": 100},
            Breakpoint.MEDIUM: {"src": "https://aaa.bbb/img?sz=m", "width": 203, "height": 200},
            Breakpoint.LARGE: {"src": "https://aaa.bbb/img?sz=l", "width": 303, "height": 300},
        },
    )


@pytest.fixture
def sd_model_banner_with_products(sponsored_product_1001, sponsored_product_1003):
    return SponsoredDisplay(
        ad_type=AdType.BANNER,
        client_id="client-id",
        ad_unit="search-top",
        uclid="abc|123|",
        creative=SponsoredDisplayCreative.SEARCH_BANNER,
        destination_url="https://foo.bar/here?boo",
        products=[sponsored_product_1001, sponsored_product_1003],
        background={
            Breakpoint.SMALL: {"src": "https://aaa.bbb/img?sz=s", "width": 103, "height": 100},
            Breakpoint.MEDIUM: {"src": "https://aaa.bbb/img?sz=m", "width": 203, "height": 200},
            Breakpoint.LARGE: {"src": "https://aaa.bbb/img?sz=l", "width": 303, "height": 300},
        },
    )


@pytest.fixture
def os_product_plid1001_sku3001():
    return OnlineSalesProduct(
        uclid="test-uclid", sku_id=3001, plid=1001, seller_id="M1234", tsin=2001
    )


@pytest.fixture
def os_product_plid1001_sku3002():
    return OnlineSalesProduct(
        uclid="test-uclid", sku_id=3002, plid=1001, seller_id="R221", tsin=2001
    )


@pytest.fixture
def os_product_plid1002_sku1001():
    return OnlineSalesProduct(
        uclid="test-uclid", sku_id=1001, plid=1002, seller_id="M1234", tsin=1111
    )


@pytest.fixture
def os_product_plid1003_sku3301():
    return OnlineSalesProduct(
        uclid="test-uclid", sku_id=3301, plid=1003, seller_id="M11111343", tsin=1111234
    )


@pytest.fixture
def os_sd_single_product(
    os_product_plid1001_sku3001, os_product_plid1001_sku3002, os_product_plid1002_sku1001
):
    return OnlineSalesDisplay(
        ad_type="product",
        client_id="client-id",
        ad_unit="search-top",
        uclid="abc|123|os_sd_single_product",
        creative=OnlineSalesCreative.SINGLE_PRODUCT,
        products=[
            os_product_plid1001_sku3001,
            os_product_plid1001_sku3002,
            os_product_plid1002_sku1001,
        ],
    )


@pytest.fixture
def os_sd_multi_product_3(
    os_product_plid1001_sku3001, os_product_plid1001_sku3002, os_product_plid1002_sku1001
):
    return OnlineSalesDisplay(
        ad_type="product",
        client_id="client-id",
        ad_unit="search-top",
        uclid="abc|123|os_sd_multi_product_3",
        creative=OnlineSalesCreative.MULTI_PRODUCT_3,
        products=[
            os_product_plid1001_sku3001,
            os_product_plid1001_sku3002,
            os_product_plid1002_sku1001,
        ],
    )


@pytest.fixture
def os_sd_search_banner_product_no_url(
    request, os_product_plid1001_sku3001, os_product_plid1001_sku3002, os_product_plid1002_sku1001
):
    return OnlineSalesDisplay(
        ad_type="banner",
        client_id="client-id",
        ad_unit="search-top",
        uclid="abc|123|os_sd_search_banner_product_no_url",
        creative=OnlineSalesCreative.SEARCH_BANNER,
        products=[
            os_product_plid1001_sku3001,
            os_product_plid1001_sku3002,
            os_product_plid1002_sku1001,
        ],
        images={
            "bg_img_src_300x50": "img://bg_img_src_300x50",
            "bg_img_src_728x90": "img://bg_img_src_728x90",
            "bg_img_src_1292x120": "img://bg_img_src_1292x120",
        },
    )


@pytest.fixture
def os_sd_search_banner_top_images(
    request, os_product_plid1001_sku3001, os_product_plid1001_sku3002, os_product_plid1002_sku1001
):
    return OnlineSalesDisplay(
        ad_type="banner",
        client_id="client-id",
        ad_unit="search-top",
        uclid="abc|123|os_sd_search_banner_top_images",
        creative=OnlineSalesCreative.SEARCH_BANNER_TOP,
        products=[],
        destination_url="new://top/banner",
        images={
            "bg_img_src_320x100": "img://bg_img_src_320x100",
            "bg_img_src_728x90": "img://bg_img_src_728x90",
            "bg_img_src_1292x120": "img://bg_img_src_1292x120",
        },
    )


@pytest.fixture
def os_sd_bad_creative(
    os_product_plid1001_sku3001, os_product_plid1001_sku3002, os_product_plid1002_sku1001
):
    return OnlineSalesDisplay(
        ad_type="product",
        client_id="client-id",
        ad_unit="search-top",
        uclid="abc|123|os_sd_bad_creative",
        creative=OnlineSalesCreative.UNKNOWN,  # We don't know what this one is yet
        products=[
            os_product_plid1001_sku3001,
            os_product_plid1001_sku3002,
            os_product_plid1002_sku1001,
        ],
    )


@pytest.fixture
def os_sd_rhb_product(
    os_product_plid1001_sku3001,
    os_product_plid1001_sku3002,
    os_product_plid1002_sku1001,
    os_product_plid1003_sku3301,
):
    return OnlineSalesDisplay(
        ad_type="banner",
        client_id="client-id",
        ad_unit="rhb-slot-1",
        uclid="abc|123|os_sd_rhb_product",
        creative=OnlineSalesCreative.HOMEPAGE_RIGHT_HAND_BANNER,
        products=[
            os_product_plid1001_sku3001,
            os_product_plid1001_sku3002,
            os_product_plid1002_sku1001,
            os_product_plid1003_sku3301,
        ],
        images={"bg_img_src_300x355": "use://this.image"},
    )


@pytest.fixture
def os_sd_rhb_banner_with_products(
    os_product_plid1001_sku3001,
    os_product_plid1001_sku3002,
    os_product_plid1002_sku1001,
    os_product_plid1003_sku3301,
):
    return OnlineSalesDisplay(
        ad_type="banner",
        client_id="client-id",
        ad_unit="rhb-slot-2",
        uclid="abc|123|os_sd_rhb_banner_with_products",
        creative=OnlineSalesCreative.HOMEPAGE_RIGHT_HAND_BANNER,
        products=[
            os_product_plid1001_sku3001,
            os_product_plid1001_sku3002,
            os_product_plid1002_sku1001,
            os_product_plid1003_sku3301,
        ],
        images={"bg_img_src_300x355": "use://this.image"},
    )


@pytest.fixture
def os_sd_rhb_banner_no_products():
    return OnlineSalesDisplay(
        ad_type="banner",
        client_id="client-id",
        ad_unit="rhb-slot-3",
        uclid="abc|123|os_sd_rhb_banner_no_products",
        creative=OnlineSalesCreative.HOMEPAGE_RIGHT_HAND_BANNER,
        products=[],
        destination_url="not://ignored/url",
        images={"bg_img_src_300x355": "use://this.image/also"},
    )


@pytest.fixture
def mock_catalogue_aggregator_integration(mocker):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    catalogue_integration = CatalogueAggregatorIntegration(
        aggregator_client=mocker.Mock(),
        config=mocker.Mock(),
        stats_client=mocker.Mock(),
        memcache=mocker.Mock(),
    )
    catalogue_integration.get_offer_ids_for_plids = mocker.Mock(return_value=[1, 2, 3])
    return catalogue_integration
