import pytest

from sponsored_ads_service.errors import ConfigurationError

pytestmark = pytest.mark.utils


@pytest.fixture(autouse=True)
def localcache_utils():
    """
    Override the global `localcache_utils` fixture as we want to test it here
    """
    ...


@pytest.fixture(autouse=True)
def mock_ttl_cache(mocker):
    return mocker.patch("cachetools.TTLCache")


@pytest.fixture
def cached_func(mock_decorator):
    from sponsored_ads_service.utils.localcache import LocalcacheUtils

    @mock_decorator(x=1)  # Testing that decorator order does not effect it
    @LocalcacheUtils.cached(ttl=100, maxsize=3, stats_key="test")
    @mock_decorator(y=2)  # Testing that decorator order does not effect it
    def wrapped(a, b, c=1):
        return 10

    return wrapped


def test_cached_hit(mocker, cached_func):
    from sponsored_ads_service.utils.hash import HashUtils
    from sponsored_ads_service.utils.localcache import LocalcacheUtils

    LocalcacheUtils._localcache_enabled = True
    key = [("a", 1), ("b", 2), ("c", 3)]
    mock_hashfunc = mocker.patch.object(HashUtils, "hashfunc", return_value=key)
    mock_get_call = mocker.patch.object(LocalcacheUtils, "_get", return_value=(True, 10))

    output = cached_func(1, 2, c=3)
    mock_hashfunc.assert_called_with(mocker.ANY, 1, 2, c=3)
    mock_get_call.assert_called_with(cached_func._localcache, key, stats_key="test")
    assert output == 10


def test_cached_miss(mocker, cached_func):
    from sponsored_ads_service.utils.hash import HashUtils
    from sponsored_ads_service.utils.localcache import LocalcacheUtils

    LocalcacheUtils._localcache_enabled = True
    key = [("a", 1), ("b", 2), ("c", 3)]
    mock_hashfunc = mocker.patch.object(HashUtils, "hashfunc", return_value=key)
    mock_get_call = mocker.patch.object(LocalcacheUtils, "_get", return_value=(False, None))

    mock_set_call = mocker.patch.object(LocalcacheUtils, "_set", return_value=True)
    output = cached_func(1, 2, c=3)
    mock_hashfunc.assert_called_with(mocker.ANY, 1, 2, c=3)
    mock_get_call.assert_called_with(cached_func._localcache, key, stats_key="test")
    mock_set_call.assert_called_with(cached_func._localcache, key, 10, stats_key="test")
    assert output == 10


def test_cache_disabled(mocker, cached_func):
    from sponsored_ads_service.utils.hash import HashUtils
    from sponsored_ads_service.utils.localcache import LocalcacheUtils

    LocalcacheUtils._localcache_enabled = False
    mock_hashfunc = mocker.patch.object(HashUtils, "hashfunc")
    mock_get_call = mocker.patch.object(LocalcacheUtils, "_get")
    mock_set_call = mocker.patch.object(LocalcacheUtils, "_set")

    output = cached_func(1, 2, c=3)
    assert mock_hashfunc.call_count == 0
    assert mock_get_call.call_count == 0
    assert mock_set_call.call_count == 0
    assert output == 10


@pytest.mark.parametrize(
    ("key", "expected"), [("a", (True, 10)), ("b", (True, None)), ("c", (False, None))]
)
def test_cache_get(mocker, key, expected):
    from sponsored_ads_service.utils.localcache import LocalcacheUtils

    cache = {"a": 10, "b": None}
    output = LocalcacheUtils._get(cache, key, stats_key="test")
    assert output == expected


def test_cache_set(mocker):
    from sponsored_ads_service.utils.localcache import LocalcacheUtils

    cache = {"a": 10}
    output = LocalcacheUtils._set(cache, "b", "value", stats_key="test")
    assert cache == {"a": 10, "b": "value"}
    assert output is True


def test_cache_failure(mocker):
    from sponsored_ads_service.utils.localcache import LocalcacheUtils

    cache = {"a": 10}
    output = LocalcacheUtils._set(cache, ["invalid-key"], "value", stats_key="test")
    assert cache == {"a": 10}
    assert output is False


def test_cached_from_config(mocker):
    """
    This is a test that sadly mocks out both of the only 2 lines it tests.
    Trying to let the cached function operate ends up calling existing mocked objects
    and returning invalid results. If/when we fix those we can make this less mocky.
    """
    import sponsored_ads_service.utils.localcache as module
    from sponsored_ads_service.utils.localcache import LocalcacheUtils

    mock_context = mocker.MagicMock()
    mock_config = mocker.patch.object(module, "SponsoredAdsConfig").return_value
    mock_getter = mock_config.get_localcache_context
    mock_getter.return_value = mock_context

    mock_cached = mocker.patch.object(LocalcacheUtils, "cached")

    @LocalcacheUtils.cached_from_config("qwecking_ducks")
    def func_1(a, c=1):
        return 10

    mock_getter.assert_called_once_with("qwecking_ducks")
    mock_cached.assert_called_once_with(
        stats_key="qwecking_ducks",
        ttl=mock_context.ttl,
        maxsize=mock_context.maxsize,
        enabled=mock_context.enabled,
    )


@pytest.mark.parametrize("name", ["", "aa.bb", "aa-bb"])
def test_cached_from_config_bad_key(mocker, name):
    from sponsored_ads_service.utils.localcache import LocalcacheUtils

    with pytest.raises(ConfigurationError):

        @LocalcacheUtils.cached_from_config(name)
        def func_1(a, c=1):
            return 10
