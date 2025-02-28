from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from cache_client import MemcachedClient
    from tal_stats_client import StatsClient

_T = TypeVar("_T")

logger = logging.getLogger(__name__)


class Memcache:
    def __init__(
        self,
        cache_client: MemcachedClient,
        stats_client: StatsClient,
        service_version: str,
    ) -> None:
        self._client = cache_client
        self._stats_client = stats_client
        self._service_version = service_version

    def get(self, context: str, key: str) -> _T | None:
        result = None
        try:
            result = self._client.get(f"{self._get_key_prefix(context)}.{key}")
            if result:
                self._stats_client.incr(self._get_stats_key(context, "hit"))
            else:
                self._stats_client.incr(self._get_stats_key(context, "miss"))
        except Exception:
            self._stats_client.incr(self._get_stats_key(context, "exception"))
            logger.exception("Failed to get from memcache", extra={"context": context, "key": key})
        return result

    def set(self, context: str, key: str, data: _T, ttl: int) -> None:
        try:
            self._client.set(
                f"{self._get_key_prefix(context)}.{key}", data, ttl=self._with_jitter(ttl)
            )
            self._stats_client.incr(self._get_stats_key(context, "set"))
        except Exception:
            self._stats_client.incr(self._get_stats_key(context, "exception"))
            logger.exception(
                "Failed to set to memcache",
                extra={"context": context, "key": key, "value": data, "ttl": ttl},
            )

    def get_multi(self, context: str, keys: list[str]) -> dict[str, _T]:
        results = {}
        try:
            results = self._client.get_multi(keys, key_prefix=self._get_key_prefix(context))
            if results:
                self._stats_client.incr(self._get_stats_key(context, "hit"), len(results))
            if misses := (set(keys) - set(results.keys())):
                self._stats_client.incr(self._get_stats_key(context, "miss"), len(misses))
        except Exception:
            self._stats_client.incr(self._get_stats_key(context, "exception"))
            logger.exception(
                "Failed to get_multi from memcache", extra={"context": context, "keys": keys}
            )
        return results

    def set_multi(self, context: str, data: dict[str, _T], ttl: int) -> None:
        try:
            self._client.set_multi(
                data, key_prefix=self._get_key_prefix(context), ttl=self._with_jitter(ttl)
            )
            self._stats_client.incr(self._get_stats_key(context, "set"), len(data))
        except Exception:
            self._stats_client.incr(self._get_stats_key(context, "exception"))
            logger.exception(
                "Failed to set_multi to memcache",
                extra={"context": context, "data": data, "ttl": ttl},
            )

    def _get_key_prefix(self, context: str) -> str:
        return f"{self._service_version}.{context}"

    def _get_stats_key(self, context: str, operation: str) -> str:
        return f"caching.memcache.{context}.{operation}"

    @classmethod
    def _with_jitter(cls, ttl: int) -> int:
        """Add a percentage "jitter" to the given TTL to avoid thundering herd"""
        return int(random.uniform(int(ttl * 0.9), int(ttl * 1.1)))
