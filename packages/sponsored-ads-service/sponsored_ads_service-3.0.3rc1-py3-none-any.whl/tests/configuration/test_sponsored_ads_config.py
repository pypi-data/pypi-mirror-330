import os

import pytest
from tal_service_config import FORMAT_LIST_OF_TUPLE

from sponsored_ads_service.configuration.sponsored_ads_config import (
    LocalcacheContext,
    MemcacheContext,
)
from sponsored_ads_service.errors import ConfigurationError
from sponsored_ads_service.models.validation import SponsoredProductsValidationConfig

pytestmark = pytest.mark.configuration


@pytest.fixture(autouse=True)
def config(mocker):
    """
    Override the global `config` fixture which usually mocks out the
    `SponsoredAdsConfig` with a mock of just the `tal_service_config.ServiceConfig`
    """
    mock = mocker.patch("tal_service_config.ServiceConfig")
    return mock.return_value


def test_load_configuration(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig
    from sponsored_ads_service.configuration import sponsored_ads_config as module

    mock_service_config = mocker.patch.object(module, "ServiceConfig")
    sponsored_ads_config = SponsoredAdsConfig()
    assert mock_service_config.call_count == 1

    output = sponsored_ads_config._load_configuration()  # Re-call _load_configuration
    assert mock_service_config.call_count == 1  # Assert not called again
    assert output == mock_service_config.return_value


def test_service_lookup(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    host_port = ["192.168.0.1:8000"]
    mock_call = mocker.patch.object(service_config.config, "find_service", return_value=host_port)
    output = service_config.service_lookup("test-service")
    mock_call.assert_called_with("test-service")
    assert output == host_port


def test_get_version(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    mock_distribution = mocker.Mock()
    mock_distribution.version = "1.0.0"
    mock_call = mocker.patch("pkg_resources.get_distribution", return_value=mock_distribution)
    output = service_config.get_version()
    mock_call.assert_called_with("sponsored_ads_service")
    assert output == "1.0.0"


def test_get_statsd_settings(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    endpoints = [("192.168.0.1", "8000")]
    mock_call = mocker.patch.object(service_config.config, "find_service", return_value=endpoints)
    output = service_config.get_statsd_settings()
    mock_call.assert_called_with("statsd", protocol="udp", format=FORMAT_LIST_OF_TUPLE)
    expected = {
        "service_name_prefix": "sponsored-ads-service",
        "host": "192.168.0.1",
        "port": "8000",
        "include_fqdn": False,
    }
    assert output == expected


def test_get_cache_settings(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    host_port = ["192.168.0.1:8000"]
    mock_call = mocker.patch.object(service_config, "service_lookup", return_value=host_port)
    output = service_config.get_cache_settings()
    mock_call.assert_called_with("mcrouter")
    expected = {
        "host_port": ["192.168.0.1:8000"],
        "namespace": "sponsored-ads-service-test",
        "socket_timeout": 5,
    }
    assert output == expected


def test_get_sentry_settings(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    mock_call = mocker.patch.object(SponsoredAdsConfig, "get_version", return_value="1.0.0")
    output = service_config.get_sentry_settings()
    expected = {
        "release": "1.0.0",
        "environment": "test",
        "dsn": "1234",
    }
    mock_call.assert_called_with()
    assert output == expected


def test_get_sentry_settings_disabled(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(os.environ, {"SENTRY_ENABLED": "false"})
    service_config = SponsoredAdsConfig()
    output = service_config.get_sentry_settings()
    assert output is None


def test_get_timeouts(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    assert service_config.get_cms_nav_timeout() == 1000
    assert service_config.get_cat_legacy_service_timeout() == 1000
    assert service_config.get_cat_aggregator_service_timeout() == 1000
    assert service_config.get_cat_api_service_timeout() == 1000
    assert service_config.get_online_sales_timeout() == 1000


def test_onlinesales_ids(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    assert service_config.get_sponsored_products_client_id() == "1234"
    assert service_config.get_onlinesales_ad_slot_id() == "1"
    assert service_config.get_sponsored_products_plid_limit() == 10
    assert service_config.get_sponsored_display_client_id() == "5678"
    assert service_config.get_sponsored_display_search_filters_plid_limit() == 32


def test_get_link_data_hostname():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    assert service_config.get_link_data_hostname() == "www.foo.bar"


def test_get_localcache_enabled():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    assert service_config.get_localcache_enabled() is True


def test_get_circuitbreakers():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    assert service_config.get_cat_aggregator_circuitbreaker_enabled() is True
    assert service_config.get_cat_api_circuitbreaker_enabled() is True
    assert service_config.get_onlinesales_circuitbreaker_enabled() is True
    assert service_config.get_onlinesales_circuitbreaker_reset_timeout_homepage() == 5
    assert service_config.get_onlinesales_circuitbreaker_reset_timeout_default() == 10


def test_get_sponsored_products_validation_config():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    output = service_config.get_sponsored_products_validation_config()
    expected = SponsoredProductsValidationConfig(
        validate_active_and_available=True,
        validate_attribute=True,
        validate_buybox=False,
        validate_stock=True,
        validate_images=True,
        validate_promo_price=True,
        validate_promo_quantity=True,
    )
    assert output == expected


def test_get_widget_product_title():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()

    assert service_config.get_widget_product_title() == "Recommended Products"


def test_get_widget_deals_title():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()

    assert service_config.get_widget_deals_title() == "Dealer's Choice"


def test_get_sponsored_products_backfill_count():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    assert service_config.get_sponsored_products_deals_backfill_count() == 6


def test_get_sponsored_products_serve_count():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    assert service_config.get_sponsored_products_deals_serve_count() == 12


def test_get_sponsored_products_per_deals_widget():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    service_config = SponsoredAdsConfig()
    assert service_config.get_sponsored_products_deals_products_per_widget() == 6


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        (
            {"LOCALCACHE_MADE_UP_TTL": "123", "LOCALCACHE_MADE_UP_MAXSIZE": "45"},
            LocalcacheContext(enabled=True, ttl=123, maxsize=45),
        ),
        (
            {
                "LOCALCACHE_MADE_UP_ENABLED": "false",
                "LOCALCACHE_MADE_UP_TTL": "123",
                "LOCALCACHE_MADE_UP_MAXSIZE": "45",
            },
            LocalcacheContext(enabled=False, ttl=0, maxsize=0),
        ),
        (
            {
                "LOCALCACHE_MADE_UP_ENABLED": "false",
            },
            LocalcacheContext(enabled=False, ttl=0, maxsize=0),
        ),
    ],
)
def test_get_localcache_context_env(mocker, env, expected):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(os.environ, env)
    output = SponsoredAdsConfig().get_localcache_context("made_up")
    assert output == expected


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        (
            {},
            LocalcacheContext(enabled=True, ttl=1801, maxsize=31),
        ),
        (
            {
                "LOCALCACHE_CATEGORY_BY_ID_TTL": "111",
            },
            LocalcacheContext(enabled=True, ttl=111, maxsize=31),
        ),
        (
            {
                "LOCALCACHE_CATEGORY_BY_ID_MAXSIZE": "222",
            },
            LocalcacheContext(enabled=True, ttl=1801, maxsize=222),
        ),
        (
            {
                "LOCALCACHE_CATEGORY_BY_ID_TTL": "333",
                "LOCALCACHE_CATEGORY_BY_ID_MAXSIZE": "444",
            },
            LocalcacheContext(enabled=True, ttl=333, maxsize=444),
        ),
        (
            {
                "LOCALCACHE_CATEGORY_BY_ID_ENABLED": "false",
            },
            LocalcacheContext(enabled=False, ttl=0, maxsize=0),
        ),
    ],
)
def test_get_localcache_context_defined(mocker, env, expected):
    """Test a value that is defined in the INI file. Does it work, can we override?"""
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(os.environ, env)
    output = SponsoredAdsConfig().get_localcache_context("category_by_id")
    assert output == expected


def test_get_localcache_context_env_no_ttl(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(
        os.environ,
        {"LOCALCACHE_MADE_UP_MAXSIZE": "45"},
    )

    with pytest.raises(ConfigurationError) as exc_info:
        SponsoredAdsConfig().get_localcache_context("made_up")

    assert ".made_up_ttl" in str(exc_info.value)


def test_get_localcache_context_env_no_maxsize(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(
        os.environ,
        {"LOCALCACHE_MADE_UP_TTL": "111"},
    )

    with pytest.raises(ConfigurationError) as exc_info:
        SponsoredAdsConfig().get_localcache_context("made_up")

    assert ".made_up_maxsize" in str(exc_info.value)


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        (
            {"MEMCACHE_MADE_UP_TTL": "123"},
            MemcacheContext(enabled=True, ttl=123),
        ),
        (
            {
                "MEMCACHE_MADE_UP_ENABLED": "no",
                "MEMCACHE_MADE_UP_TTL": "123",
            },
            MemcacheContext(enabled=False, ttl=0),
        ),
        (
            {
                "MEMCACHE_MADE_UP_ENABLED": "no",
            },
            MemcacheContext(enabled=False, ttl=0),
        ),
    ],
)
def test_get_memcache_context_env(mocker, env, expected):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(os.environ, env)
    output = SponsoredAdsConfig().get_memcache_context("made_up")
    assert output == expected


@pytest.mark.parametrize(
    ("context", "env", "expected"),
    [
        (
            "category_by_id",
            {},
            MemcacheContext(enabled=True, ttl=3603),
        ),
        (
            "category_by_id",
            {"MEMCACHE_CATEGORY_BY_ID_TTL": "999"},
            MemcacheContext(enabled=True, ttl=999),
        ),
    ],
)
def test_get_memcache_context_defined(mocker, context, env, expected):
    """Test a value that is defined in the INI file. Does it work, can we override?"""
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(os.environ, env)
    output = SponsoredAdsConfig().get_memcache_context(context)
    assert output == expected


def test_get_memcache_context_env_no_ttl(mocker):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    with pytest.raises(ConfigurationError) as exc_info:
        SponsoredAdsConfig().get_memcache_context("made_up")

    assert ".made_up_ttl" in str(exc_info.value)


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        (
            {},
            False,  # Disabled by default until OnlineSales migration is done
        ),
        (
            {"ROLLOUT_FLAG_SEARCH_BANNER_REMAP": "true"},
            True,
        ),
        (
            {"ROLLOUT_FLAG_SEARCH_BANNER_REMAP": "false"},
            False,
        ),
    ],
)
def test_get_rollout_flag_search_banner_remap(mocker, env, expected):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(os.environ, env)
    service_config = SponsoredAdsConfig()
    assert service_config.get_rollout_flag_search_banner_remap() == expected


def test_circuitbreaker_config_enabled():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    # === Setup ===
    cfg = SponsoredAdsConfig()

    # === Execute ===
    output = cfg.get_circuitbreaker_config("onlinesales")

    # === Verify ===
    assert output.enabled is True
    assert output.reset_timeout_s == 10
    assert output.max_fail == 3


def test_circuitbreaker_config_disabled():
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    # === Setup ===
    cfg = SponsoredAdsConfig()

    # === Execute ===
    output = cfg.get_circuitbreaker_config("fake_service")

    # === Verify ===
    assert output.enabled is False
    assert output.reset_timeout_s == 11
    assert output.max_fail == 4


@pytest.mark.parametrize(
    ("env", "expected_ttl", "expected_enabled"),
    [
        (
            {
                "MEMCACHE_CATALOGUE_AGGREGATOR_TTL": "21",
                "MEMCACHE_CATALOGUE_AGGREGATOR_ENABLED": "false",
            },
            0,
            False,
        ),
        ({}, 601, True),
    ],
)
def test_get_catalogue_aggregator_cache_ttl(mocker, env, expected_ttl, expected_enabled):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(os.environ, env)
    service_config = SponsoredAdsConfig()
    cache_context = service_config.get_catalogue_aggregator_cache_context()
    assert cache_context.enabled == expected_enabled
    assert cache_context.ttl == expected_ttl


@pytest.mark.parametrize(
    ("env", "expected_ttl", "expected_enabled"),
    [
        (
            {"MEMCACHE_DEPARTMENTS_TTL": "21", "MEMCACHE_DEPARTMENTS_ENABLED": "False"},
            0,
            False,
        ),
        ({}, 3604, True),
    ],
)
def test_get_departments_cache_ttl(mocker, env, expected_ttl, expected_enabled):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(os.environ, env)
    service_config = SponsoredAdsConfig()
    cache_context = service_config.get_departments_cache_context()
    assert cache_context.enabled == expected_enabled
    assert cache_context.ttl == expected_ttl


@pytest.mark.parametrize(
    ("env", "expected_ttl", "expected_enabled"),
    [
        (
            {"MEMCACHE_CATEGORY_BY_ID_TTL": "21", "MEMCACHE_CATEGORY_BY_ID_ENABLED": "false"},
            0,
            False,
        ),
        ({}, 3603, True),
    ],
)
def test_get_category_by_id_cache_ttl(mocker, env, expected_ttl, expected_enabled):
    from sponsored_ads_service.configuration import SponsoredAdsConfig

    mocker.patch.dict(os.environ, env)
    service_config = SponsoredAdsConfig()
    cache_context = service_config.get_category_by_id_cache_context()
    assert cache_context.enabled == expected_enabled
    assert cache_context.ttl == expected_ttl
