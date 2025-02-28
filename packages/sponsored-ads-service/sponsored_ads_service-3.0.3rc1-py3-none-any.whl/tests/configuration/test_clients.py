import pytest

pytestmark = pytest.mark.configuration


@pytest.fixture(autouse=True)
def clients(request, config, mocker):
    """
    Override the global `clients` fixture which usually mocks out the
    `Clients` with a mock of just what is needed for the tests
    """
    from sponsored_ads_service.configuration import Clients

    mark = request.node.get_closest_marker("configuration")
    kwargs = mark.kwargs if mark else {}
    if kwargs.get("override_fixture") != "clients":
        mocker.patch.object(Clients, "__init__", return_value=None)
        Clients._config = config


@pytest.fixture(autouse=True)
def localcache_utils():
    """
    Override the global `localcache_utils` fixture as it causes issues when testing
    the Clients
    """
    ...


@pytest.fixture(autouse=True)
def memcache_utils():
    """
    Override the global `memcache_utils` fixture as it causes issues when testing
    the Clients
    """
    ...


@pytest.fixture
def mock_configure(mocker):
    from sponsored_ads_service.configuration import Clients

    mocker.patch.object(Clients, "_configure")


def test_configure(mocker):
    from sponsored_ads_service.configuration import Clients
    from sponsored_ads_service.configuration import clients as module

    mock_config = mocker.patch.object(module, "SponsoredAdsConfig").return_value
    mock_statsd = mocker.patch.object(Clients, "_configure_statsd_client")
    mock_cache = mocker.patch.object(Clients, "_configure_cache_client")
    mock_cms_nav = mocker.patch.object(Clients, "_configure_cms_nav_client")
    mock_catalogue_legacy = mocker.patch.object(Clients, "_configure_catalogue_legacy_client")
    mock_catalogue_aggregator = mocker.patch.object(
        Clients, "_configure_catalogue_aggregator_client"
    )

    clients = Clients()
    clients._config = None
    clients._configure()

    assert clients._config == mock_config
    mock_statsd.assert_called_with()
    mock_cache.assert_called_with()
    mock_cms_nav.assert_called_with()
    mock_catalogue_legacy.assert_called_with()
    mock_catalogue_aggregator.assert_called_with()


def test_stats_client(mocker):
    from sponsored_ads_service.configuration import Clients
    from sponsored_ads_service.configuration import clients as module

    mock_client = mocker.patch.object(module, "StatsClient").return_value
    settings = {
        "service_name_prefix": "sponsored-ads-service",
        "host": "192.168.0.1",
        "port": "8000",
        "include_fqdn": False,
    }
    mock_config_call = mocker.patch.object(
        Clients._config, "get_statsd_settings", return_value=settings
    )
    Clients()._configure_statsd_client()
    mock_config_call.assert_called_with()
    mock_client.configure_for_service.assert_called_with(
        service_name="sponsored-ads-service",
        stats_host="192.168.0.1",
        stats_port="8000",
        include_fqdn=False,
    )


def test_cache_client(mocker):
    from sponsored_ads_service.configuration import Clients
    from sponsored_ads_service.configuration import clients as module

    mock_client = mocker.patch.object(module, "MemcachedClient").return_value
    settings = {
        "host_port": ["192.168.0.1:8000"],
        "namespace": "sponsored-ads-service",
        "socket_timeout": 5,
    }
    mock_config_call = mocker.patch.object(
        Clients._config, "get_cache_settings", return_value=settings
    )
    Clients()._configure_cache_client()
    mock_config_call.assert_called_with()
    mock_client.configure.assert_called_with(
        hosts_and_ports=["192.168.0.1:8000"],
        namespace="sponsored-ads-service",
        socket_timeout=5,
    )


def test_cms_nav(mocker):
    from sponsored_ads_service.configuration import Clients
    from sponsored_ads_service.configuration import clients as module

    mock_client = mocker.patch.object(module, "CmsNavigationClient")
    endpoints = ["192.168.0.1:8000"]
    timeout = 1000
    mock_lookup_call = mocker.patch.object(
        Clients._config, "service_lookup", return_value=endpoints
    )
    mock_timeout_call = mocker.patch.object(
        Clients._config, "get_cms_nav_timeout", return_value=timeout
    )
    Clients()._configure_cms_nav_client()
    mock_lookup_call.assert_called_with("cms_navigation_service")
    mock_timeout_call.assert_called_with()
    mock_client.assert_called_with(endpoints=endpoints, recv_timeout=timeout)


def test_catalogue_legacy_service(mocker):
    from sponsored_ads_service.configuration import Clients
    from sponsored_ads_service.configuration import clients as module

    mock_client = mocker.patch.object(module, "CatalogueLegacyServiceClient")
    endpoints = ["192.168.0.1:8000"]
    timeout = 1000
    mock_lookup_call = mocker.patch.object(
        Clients._config, "service_lookup", return_value=endpoints
    )
    mock_timeout_call = mocker.patch.object(
        Clients._config, "get_cat_legacy_service_timeout", return_value=timeout
    )
    Clients()._configure_catalogue_legacy_client()
    mock_lookup_call.assert_called_with("s4f_catalogue_legacy")
    mock_timeout_call.assert_called_with()
    mock_client.assert_called_with(endpoints=endpoints, recv_timeout=timeout)


def test_catalogue_aggregator_service(mocker):
    from sponsored_ads_service.configuration import Clients
    from sponsored_ads_service.configuration import clients as module

    mock_client = mocker.patch.object(module, "CatalogueAggregatorHttpClient")
    endpoints = ["192.168.0.1:8000"]
    timeout = 1000
    mock_lookup_call = mocker.patch.object(
        Clients._config, "service_lookup", return_value=endpoints
    )
    mock_timeout_call = mocker.patch.object(
        Clients._config, "get_cat_aggregator_service_timeout", return_value=timeout
    )
    Clients()._configure_catalogue_aggregator_client()
    mock_lookup_call.assert_called_with("catalogue_aggregator")
    mock_timeout_call.assert_called_with()
    mock_client.assert_called_with(service_endpoint="192.168.0.1:8000", timeout_seconds=1.0)


def test_configures_once(mocker):
    from sponsored_ads_service.configuration import Clients

    clients = Clients()
    mock_item = mocker.Mock()

    # Attach mock
    clients.stats_client = mock_item
    clients.cache_client = mock_item
    clients.cms_nav_client = mock_item
    clients.cat_legacy_client = mock_item
    clients.cat_aggregator_client = mock_item
    clients.cat_api_client = mock_item

    # Call configure
    clients._configure()

    # Assert the configure exited early and did not overwrite
    assert clients.stats_client == mock_item
    assert clients.cache_client == mock_item
    assert clients.cms_nav_client == mock_item
    assert clients.cat_legacy_client == mock_item
    assert clients.cat_aggregator_client == mock_item
    assert clients.cat_api_client == mock_item


@pytest.mark.configuration(override_fixture="clients")
def test_init(mocker):
    from sponsored_ads_service.configuration import Clients

    mock_configure = mocker.patch.object(Clients, "_configure")
    Clients()
    mock_configure.assert_called_with()
