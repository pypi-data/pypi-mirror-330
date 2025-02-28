import pytest

from sponsored_ads_service.errors import ConfigurationError
from sponsored_ads_service.models.caching import MemcacheHolder, MultiMemcacheResult

pytestmark = pytest.mark.utils


@pytest.fixture(autouse=True)
def memcache_utils():
    """
    Override the global `memcache_utils` fixture as we want to test it here
    """
    ...


@pytest.fixture
def cached_func(mock_decorator):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    @mock_decorator(x=1)  # Testing that decorator order does not effect it
    @MemcacheUtils.cached("cache", ttl=100)
    @mock_decorator(y=2)  # Testing that decorator order does not effect it
    def wrapped(a, b, c=1):
        return 10

    return wrapped


def test_cached_hit(mocker, cached_func):
    from sponsored_ads_service.utils.hash import HashUtils
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mock_hashfunc = mocker.patch.object(
        HashUtils, "hashfunc", return_value=[("a", 1), ("b", 2), ("c", 3)]
    )
    mock_get_call = mocker.patch.object(MemcacheUtils, "get", return_value=(True, 10))
    key = "a:1|b:2|c:3"
    output = cached_func(1, 2, c=3)
    mock_hashfunc.assert_called_with(mocker.ANY, 1, 2, c=3)
    mock_get_call.assert_called_with("cache", key, cache_nones=False)
    assert output == 10


def test_cached_miss(mocker, cached_func):
    from sponsored_ads_service.utils.hash import HashUtils
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mock_hashfunc = mocker.patch.object(
        HashUtils, "hashfunc", return_value=[("a", 1), ("b", 2), ("c", 3)]
    )
    mock_get_call = mocker.patch.object(MemcacheUtils, "get", return_value=(False, None))
    mock_add_call = mocker.patch.object(MemcacheUtils, "add", return_value=True)
    key = "a:1|b:2|c:3"
    output = cached_func(1, 2, c=3)
    mock_hashfunc.assert_called_with(mocker.ANY, 1, 2, c=3)
    mock_get_call.assert_called_with("cache", key, cache_nones=False)
    mock_add_call.assert_called_with("cache", key, 10, ttl=100, cache_nones=False)
    assert output == 10


@pytest.mark.parametrize(("is_valid", "result"), [(True, 10), (False, None)])
def test_get(mocker, is_valid, result):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mock_prefix = mocker.patch.object(MemcacheUtils, "_build_prefix", return_value="prefix_cache")
    mock_call = mocker.patch.object(
        MemcacheUtils._cache_client, "get", return_value=MemcacheHolder(10)
    )
    mock_is_valid = mocker.patch.object(
        MemcacheUtils, "_is_valid_cache_value", return_value=is_valid
    )
    output = MemcacheUtils.get("cache", "key")
    mock_prefix.assert_called_with("cache")
    mock_call.assert_called_with("prefix_cache.key")
    mock_is_valid.assert_called_with(MemcacheHolder(10), cache_nones=False)
    assert output == (is_valid, result)


def test_add_valid(mocker):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mock_prefix = mocker.patch.object(MemcacheUtils, "_build_prefix", return_value="prefix_cache")
    mock_is_valid = mocker.patch.object(MemcacheUtils, "_is_valid_cache_value", return_value=True)
    mock_jitter = mocker.patch.object(MemcacheUtils, "_add_jitter", return_value=110)
    mock_add = mocker.patch.object(MemcacheUtils._cache_client, "add", return_value=True)
    output = MemcacheUtils.add("cache", "key", 10, ttl=100)
    mock_prefix.assert_called_with("cache")
    mock_is_valid.assert_called_with(MemcacheHolder(10), cache_nones=False)
    mock_jitter.assert_called_with(100)
    mock_add.assert_called_with("prefix_cache.key", MemcacheHolder(10), ttl=110)
    assert output is True


def test_add_invalid(mocker):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mock_prefix = mocker.patch.object(MemcacheUtils, "_build_prefix", return_value="prefix_cache")
    mock_is_valid = mocker.patch.object(MemcacheUtils, "_is_valid_cache_value", return_value=False)
    output = MemcacheUtils.add("cache", "key", 10, ttl=100)
    mock_prefix.assert_called_with("cache")
    mock_is_valid.assert_called_with(MemcacheHolder(10), cache_nones=False)
    assert output is False


@pytest.mark.parametrize(
    ("keys", "cache_response", "mapping", "expected"),
    [
        (
            ["a", "b", "c"],
            {"a": MemcacheHolder(1), "b": MemcacheHolder(2), "c": MemcacheHolder(3)},
            {"a": 1, "b": 2, "c": 3},
            MultiMemcacheResult(hits={"a": 1, "b": 2, "c": 3}, misses=[]),
        ),
        (
            ["a", "b", "c"],
            {"a": MemcacheHolder(1), "b": MemcacheHolder(2)},
            {"a": 1, "b": 2},
            MultiMemcacheResult(hits={"a": 1, "b": 2}, misses=["c"]),
        ),
        (
            ["a", "b", "c"],
            {"a": MemcacheHolder(1), "b": MemcacheHolder(2), "c": MemcacheHolder(3)},
            {"a": 1, "c": 3},
            MultiMemcacheResult(hits={"a": 1, "c": 3}, misses=["b"]),
        ),
    ],
)
def test_get_multi(mocker, keys, cache_response, mapping, expected):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mock_prefix = mocker.patch.object(MemcacheUtils, "_build_prefix", return_value="prefix_cache")
    mock_get_call = mocker.patch.object(
        MemcacheUtils._cache_client, "get_multi", return_value=cache_response
    )
    mock_extract_mapping = mocker.patch.object(
        MemcacheUtils, "_extract_mapping", return_value=mapping
    )
    output = MemcacheUtils.get_multi("cache", keys)
    mock_prefix.assert_called_with("cache")
    mock_get_call.assert_called_with(keys, key_prefix="prefix_cache")
    mock_extract_mapping.assert_called_with(cache_response, cache_nones=False)
    assert output == expected


@pytest.mark.parametrize(
    ("mapping", "is_valid_side_effect", "cache_mapping", "cache_response", "expected"),
    [
        (
            {"a": 1, "b": 2, "c": 3},
            [True, True, True],
            {"a": MemcacheHolder(1), "b": MemcacheHolder(2), "c": MemcacheHolder(3)},
            [],
            [],
        ),
        (
            {"a": 1, "b": 2, "c": 3},
            [True, True, True],
            {"a": MemcacheHolder(1), "b": MemcacheHolder(2), "c": MemcacheHolder(3)},
            ["a"],
            ["a"],
        ),
        (
            {"a": 1, "b": 2, "c": 3},
            [True, True, False],
            {"a": MemcacheHolder(1), "b": MemcacheHolder(2)},
            ["a"],
            ["a", "c"],
        ),
    ],
)
def test_set_multi(mocker, mapping, is_valid_side_effect, cache_mapping, cache_response, expected):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mock_prefix = mocker.patch.object(MemcacheUtils, "_build_prefix", return_value="prefix_cache")
    mock_is_valid = mocker.patch.object(
        MemcacheUtils, "_is_valid_cache_value", side_effect=is_valid_side_effect
    )
    mock_jitter = mocker.patch.object(MemcacheUtils, "_add_jitter", return_value=110)
    mock_set_call = mocker.patch.object(
        MemcacheUtils._cache_client, "set_multi", return_value=cache_response
    )

    output = MemcacheUtils.set_multi("cache", mapping, ttl=100)
    mock_prefix.assert_called_with("cache")
    assert mock_is_valid.call_count == len(mapping.keys())
    mock_jitter.assert_called_with(100)
    mock_set_call.assert_called_with(cache_mapping, key_prefix="prefix_cache", ttl=110)
    assert output == expected


@pytest.mark.parametrize(
    ("key_prefix", "expected"),
    [("cache", "memcache_1-2-3_cache"), ("test spaces", "memcache_1-2-3_test+spaces")],
)
def test_build_prefix(mocker, key_prefix, expected):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    MemcacheUtils._service_version = "1.2.3"
    output = MemcacheUtils._build_prefix(key_prefix)
    assert output == expected


@pytest.mark.parametrize(
    ("holder", "cache_nones", "expected"),
    [
        (MemcacheHolder(1), False, True),
        (MemcacheHolder(None), False, False),
        (MemcacheHolder(None), True, True),
        (None, True, False),
    ],
)
def test_is_valid_cache_value(holder, cache_nones, expected):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    output = MemcacheUtils._is_valid_cache_value(holder, cache_nones=cache_nones)
    assert output == expected


def test_add_jitter(mocker):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mock_random = mocker.patch("random.uniform", return_value=10)
    output = MemcacheUtils._add_jitter(10)
    mock_random.assert_called_with(9, 11)
    assert output == 10


def test_extract_mapping(mocker):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mapping = {
        "a": MemcacheHolder(1),
        "b": MemcacheHolder(2),
        "c": MemcacheHolder(3),
    }
    mock_is_valid = mocker.patch.object(
        MemcacheUtils, "_is_valid_cache_value", side_effect=[True, True, False]
    )
    output = MemcacheUtils._extract_mapping(mapping)
    assert mock_is_valid.call_count == 3
    expected = {"a": 1, "b": 2}
    assert output == expected


def test_cached_from_config_with_simple_ttl(mocker):
    """
    Also see test_localcache.py::test_cached_from_config
    """
    import sponsored_ads_service.utils.legacy.memcache as module
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    mock_context = mocker.MagicMock()
    mock_config = mocker.patch.object(module, "SponsoredAdsConfig").return_value
    mock_getter = mock_config.get_memcache_context
    mock_getter.return_value = mock_context

    mock_cached = mocker.patch.object(MemcacheUtils, "cached")

    @MemcacheUtils.cached_from_config("qwecking_ducks")
    def func_1(a, c=1):
        return 10

    mock_getter.assert_called_once_with("qwecking_ducks")
    mock_cached.assert_called_once_with(
        key_prefix="qwecking_ducks",
        ttl=mock_context.ttl,
        enabled=mock_context.enabled,
        cache_nones=False,
    )


@pytest.mark.parametrize("name", ["", "aa.bb", "aa-bb"])
def test_cached_from_config_bad_key(mocker, name):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    with pytest.raises(ConfigurationError):

        @MemcacheUtils.cached_from_config(name)
        def func_1(a, c=1):
            return 10


def test_cache_disabled(mocker):
    from sponsored_ads_service.utils.legacy.memcache import MemcacheUtils

    @MemcacheUtils.cached("cache", ttl=100, enabled=False)
    def wrapped(a, b, c=1):
        return 10

    mock_get_call = mocker.patch.object(MemcacheUtils, "get")
    mock_set_call = mocker.patch.object(MemcacheUtils, "add")

    output = wrapped(1, 2, c=3)

    assert mock_get_call.call_count == 0
    assert mock_set_call.call_count == 0
    assert output == 10
