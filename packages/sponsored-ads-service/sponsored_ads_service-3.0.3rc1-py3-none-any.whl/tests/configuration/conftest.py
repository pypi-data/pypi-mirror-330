import os

import pytest


@pytest.fixture(autouse=True)
def environment(mocker):
    env_vars = {
        "TIMEOUT_CMS_NAV": "1000",
        "TIMEOUT_CAT_LEGACY_SERVICE": "1000",
        "TIMEOUT_CAT_AGGREGATOR": "1000",
        "TIMEOUT_CAT_API": "1000",
        "TIMEOUT_ONLINE_SALES": "1000",
        "SPONSORED_PRODUCTS_PLID_LIMIT": "10",
        "SPONSORED_PRODUCTS_PER_DEALS_WIDGET": "6",
        "SPONSORED_PRODUCTS_ADS_DEALS_SERVE_COUNT": "12",
        "SPONSORED_PRODUCTS_ADS_BACKFILL_COUNT": "6",
        "SPONSORED_PRODUCTS_CLIENT_ID": "1234",
        "SPONSORED_PRODUCTS_AD_SLOT_ID": "1",
        "SPONSORED_PRODUCTS_VALIDATE_ACTIVE_AND_AVAILABLE": "true",
        "SPONSORED_PRODUCTS_VALIDATE_ATTRIBUTE": "true",
        "SPONSORED_PRODUCTS_VALIDATE_BUYBOX": "false",
        "SPONSORED_PRODUCTS_VALIDATE_STOCK": "true",
        "SPONSORED_PRODUCTS_VALIDATE_IMAGES": "true",
        "SPONSORED_PRODUCTS_VALIDATE_PROMO_PRICE": "true",
        "SPONSORED_PRODUCTS_VALIDATE_PROMO_QUANTITY": "true",
        "MEMCACHE_SOCKET_TIMEOUT": "5",
        "MEMCACHE_NAMESPACE_SUFFIX": "test",
        "LOCALCACHE_ENABLED": "true",
        "TRACE_ENABLED": "true",
        "TRACE_SAMPLE_RATE": "0.5",
        "TRACE_REMOTE_IP": "192.168.0.1:8000",
        "CB_CAT_AGGREGATOR_ENABLED": "true",
        "CB_CAT_API_ENABLED": "true",
        "CB_ONLINESALES_ENABLED": "true",
        "CB_ONLINESALES_RESET_TIMEOUT_DEFAULT": "10",
        "CB_ONLINESALES_RESET_TIMEOUT_HOMEPAGE": "5",
        "ROLE": "test",
        "TAL_DOMAIN": "test.env",
        "ENVIRONMENT": "test",
        "SENTRY_ENABLED": "true",
        "SENTRY_DSN": "1234",
        "PRODUCT_WIDGET_TITLE": "Recommended Products",
        "DEALS_WIDGET_TITLE": "Dealer's Choice",
        "SPONSORED_DISPLAY_CLIENT_ID": "5678",
        "SPONSORED_DISPLAY_SEARCH_FILTERS_PLID_LIMIT": "32",
        "LINK_DATA_HOSTNAME": "www.foo.bar",
    }
    mocker.patch.dict(os.environ, env_vars)
    return env_vars
