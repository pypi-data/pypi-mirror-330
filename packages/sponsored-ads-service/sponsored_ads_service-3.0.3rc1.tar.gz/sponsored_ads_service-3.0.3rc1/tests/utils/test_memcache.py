import pytest

from sponsored_ads_service.utils.memcache import Memcache


@pytest.fixture
def cache_client(mocker):
    return mocker.MagicMock()


@pytest.fixture
def stats_client(mocker):
    return mocker.MagicMock()


class TestGet:
    @pytest.fixture(autouse=True)
    def setup(self, cache_client, stats_client):
        self._memcache = Memcache(
            cache_client=cache_client,
            stats_client=stats_client,
            service_version="1.2.3",
        )

    def test_hit(self, cache_client, stats_client):
        cache_client.get.return_value = "value"
        output = self._memcache.get("context", "key")
        cache_client.get.assert_called_once_with("1.2.3.context.key")
        stats_client.incr.assert_called_once_with("caching.memcache.context.hit")
        assert output == "value"

    def test_miss(self, cache_client, stats_client):
        cache_client.get.return_value = None
        output = self._memcache.get("context", "key")
        cache_client.get.assert_called_once_with("1.2.3.context.key")
        stats_client.incr.assert_called_once_with("caching.memcache.context.miss")
        assert output is None

    def test_exception(self, mocker, cache_client, stats_client):
        cache_client.get.side_effect = Exception
        logger = mocker.patch("sponsored_ads_service.utils.memcache.logger")
        output = self._memcache.get("context", "key")
        cache_client.get.assert_called_once_with("1.2.3.context.key")
        stats_client.incr.assert_called_once_with("caching.memcache.context.exception")
        logger.exception.assert_called_once_with(
            "Failed to get from memcache", extra={"context": "context", "key": "key"}
        )
        assert output is None


class TestSet:
    @pytest.fixture(autouse=True)
    def setup(self, cache_client, stats_client):
        self._memcache = Memcache(
            cache_client=cache_client,
            stats_client=stats_client,
            service_version="1.2.3",
        )

    def test_set(self, mocker, cache_client, stats_client):
        mock_random = mocker.patch("random.uniform", return_value=99)
        self._memcache.set("context", "key", "value", 100)
        mock_random.assert_called_once_with(90, 110)
        cache_client.set.assert_called_once_with("1.2.3.context.key", "value", ttl=99)
        stats_client.incr.assert_called_once_with("caching.memcache.context.set")

    def test_exception(self, mocker, cache_client, stats_client):
        mocker.patch("random.uniform", return_value=100)
        cache_client.set.side_effect = Exception
        logger = mocker.patch("sponsored_ads_service.utils.memcache.logger")
        self._memcache.set("context", "key", "value", 100)
        cache_client.set.assert_called_once_with("1.2.3.context.key", "value", ttl=100)
        stats_client.incr.assert_called_once_with("caching.memcache.context.exception")
        logger.exception.assert_called_once_with(
            "Failed to set to memcache",
            extra={"context": "context", "key": "key", "value": "value", "ttl": 100},
        )


class TestGetMulti:
    @pytest.fixture(autouse=True)
    def setup(self, cache_client, stats_client):
        self._memcache = Memcache(
            cache_client=cache_client,
            stats_client=stats_client,
            service_version="1.2.3",
        )

    def test_all_hits(self, cache_client, stats_client):
        cache_client.get_multi.return_value = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }
        output = self._memcache.get_multi("context", ["key1", "key2", "key3"])
        cache_client.get_multi.assert_called_once_with(
            ["key1", "key2", "key3"], key_prefix="1.2.3.context"
        )
        stats_client.incr.assert_called_once_with("caching.memcache.context.hit", 3)
        assert output == {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }

    def test_all_misses(self, cache_client, stats_client):
        cache_client.get_multi.return_value = {}
        output = self._memcache.get_multi("context", ["key1", "key2", "key3"])
        cache_client.get_multi.assert_called_once_with(
            ["key1", "key2", "key3"], key_prefix="1.2.3.context"
        )
        stats_client.incr.assert_called_once_with("caching.memcache.context.miss", 3)
        assert output == {}

    def test_partial(self, mocker, cache_client, stats_client):
        cache_client.get_multi.return_value = {"key1": "value1", "key3": "value3"}
        output = self._memcache.get_multi("context", ["key1", "key2", "key3"])
        cache_client.get_multi.assert_called_once_with(
            ["key1", "key2", "key3"], key_prefix="1.2.3.context"
        )
        stats_client.incr.assert_has_calls(
            [
                mocker.call("caching.memcache.context.hit", 2),
                mocker.call("caching.memcache.context.miss", 1),
            ]
        )
        assert output == {"key1": "value1", "key3": "value3"}

    def test_exception(self, mocker, cache_client, stats_client):
        cache_client.get_multi.side_effect = Exception
        logger = mocker.patch("sponsored_ads_service.utils.memcache.logger")
        output = self._memcache.get_multi("context", ["key1", "key2", "key3"])
        cache_client.get_multi.assert_called_once_with(
            ["key1", "key2", "key3"], key_prefix="1.2.3.context"
        )
        stats_client.incr.assert_called_once_with("caching.memcache.context.exception")
        logger.exception.assert_called_once_with(
            "Failed to get_multi from memcache",
            extra={"context": "context", "keys": ["key1", "key2", "key3"]},
        )
        assert output == {}


class TestSetMulti:
    @pytest.fixture(autouse=True)
    def setup(self, cache_client, stats_client):
        self._memcache = Memcache(
            cache_client=cache_client,
            stats_client=stats_client,
            service_version="1.2.3",
        )

    def test_set_multi(self, mocker, cache_client, stats_client):
        mock_random = mocker.patch("random.uniform", return_value=99)
        data = {"key1": "value1", "key2": "value2", "key3": "value3"}

        self._memcache.set_multi("context", data, 100)

        mock_random.assert_called_once_with(90, 110)
        cache_client.set_multi.assert_called_once_with(data, key_prefix="1.2.3.context", ttl=99)
        stats_client.incr.assert_called_once_with("caching.memcache.context.set", 3)

    def test_exception(self, mocker, cache_client, stats_client):
        mocker.patch("random.uniform", return_value=100)
        cache_client.set_multi.side_effect = Exception
        logger = mocker.patch("sponsored_ads_service.utils.memcache.logger")
        data = {"key1": "value1", "key2": "value2", "key3": "value3"}

        self._memcache.set_multi("context", data, 100)
        cache_client.set_multi.assert_called_once_with(data, key_prefix="1.2.3.context", ttl=100)
        stats_client.incr.assert_called_once_with("caching.memcache.context.exception")
        logger.exception.assert_called_once_with(
            "Failed to set_multi to memcache",
            extra={"context": "context", "data": data, "ttl": 100},
        )
