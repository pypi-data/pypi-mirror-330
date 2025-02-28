"""
TODO: Rewrite to allow dependency injection.

```python
class SomeClass:
    def __init__(self, memcache: MemcacheClient) -> None:
        self._memcache = memcache

    @memcached_method("prefix", cache=lambda self: self._memcache, ttl=100)
    def some_func(self, a: int) -> int:
        ...
```
"""

import logging
import random
from contextlib import AbstractContextManager
from functools import wraps
from typing import Any, Literal, cast

from sponsored_ads_service.configuration import Clients, SponsoredAdsConfig
from sponsored_ads_service.errors import ConfigurationError
from sponsored_ads_service.models.caching import (
    CacheResult,
    MemcacheHolder,
    MultiMemcacheResult,
)
from sponsored_ads_service.models.decorated import Decorated, DecoratedWithArgs
from sponsored_ads_service.utils.hash import HashUtils

__all__ = ["MemcacheUtils"]

logger = logging.getLogger(__name__)


class MemcacheUtils:
    """A utility class for integrating with memcache"""

    _cache_client = Clients().cache_client
    _stats_client = Clients().stats_client

    _service_version = SponsoredAdsConfig().get_version()
    _stats_key = "caching.memcache"

    @classmethod
    def cached_from_config(cls, context: str, *, cache_nones: bool = False) -> DecoratedWithArgs:
        if not context.isidentifier():
            # isidentifier gives us a good enough test, we mainly want to prevent dashes
            raise ConfigurationError(
                "Invalid memcache key for config, only use keys that can be valid "
                f"unix environment variables: '{context}'"
            )

        cache_config = SponsoredAdsConfig().get_memcache_context(context)

        return cls.cached(
            key_prefix=context,
            ttl=cache_config.ttl,
            cache_nones=cache_nones,
            enabled=cache_config.enabled,
        )

    @classmethod
    def cached(
        cls, key_prefix: str, ttl: int, cache_nones: bool = False, enabled: bool = True
    ) -> DecoratedWithArgs:
        """
        Cache the result of the given method in memcache

        Use it as:
        ```
            @MemcacheUtils.cached("cache-key", ttl=1200)
            def function_to_cache(p1, p2):
                ...
        ```
        """

        def decorator(func: Decorated[CacheResult]) -> Decorated[CacheResult]:
            @wraps(func)
            def inner(*args: Any, **kwargs: Any) -> CacheResult:
                if not enabled:
                    return func(*args, **kwargs)

                hashed_key = HashUtils.hashfunc(func, *args, **kwargs)

                # Memcache wants a string with no spaces
                key = "|".join([f"{k}:{v!s}" for k, v in hashed_key])
                key = key.replace(" ", "_")

                found, val = cls.get(key_prefix, key, cache_nones=cache_nones)
                if found:
                    return cast(CacheResult, val)
                results = func(*args, **kwargs)
                cls.add(key_prefix, key, results, ttl=ttl, cache_nones=cache_nones)
                return results

            return inner

        return decorator

    @classmethod
    def get(
        cls, key_prefix: str, key: str, cache_nones: bool = False
    ) -> tuple[bool, CacheResult | None]:
        """Gets the value for a key from the memcache, returns as (`found`, `value`)"""
        prefix = cls._build_prefix(key_prefix)
        with cls._cache_command_stats_timer("get"):
            response = cls._cache_client.get(f"{prefix}.{key}")
        if cls._is_valid_cache_value(response, cache_nones=cache_nones):
            cls._stats_client.incr(f"{cls._stats_key}.{key_prefix}.hit")
            return True, response.value
        cls._stats_client.incr(f"{cls._stats_key}.{key_prefix}.miss")
        return False, None

    @classmethod
    def add(
        cls,
        key_prefix: str,
        key: str,
        value: CacheResult,
        ttl: int,
        cache_nones: bool = False,
    ) -> bool:
        """Adds the value for a key into the memcache, if it does not exist"""
        prefix = cls._build_prefix(key_prefix)
        val = MemcacheHolder(value)
        if cls._is_valid_cache_value(val, cache_nones=cache_nones):
            cls._stats_client.incr(f"{cls._stats_key}.{key_prefix}.set")
            with cls._cache_command_stats_timer("add"):
                response = cls._cache_client.add(f"{prefix}.{key}", val, ttl=cls._add_jitter(ttl))
            return bool(response)
        return False

    @classmethod
    def get_multi(
        cls, key_prefix: str, keys: list[str], cache_nones: bool = False
    ) -> MultiMemcacheResult[CacheResult]:
        """Fetch multiple entries from memcache in a single call"""
        prefix = cls._build_prefix(key_prefix)
        with cls._cache_command_stats_timer("get_multi"):
            response = cls._cache_client.get_multi([str(k) for k in keys], key_prefix=prefix)
        hits: dict[str, CacheResult] = cls._extract_mapping(response, cache_nones=cache_nones)
        misses = list(set(keys) - set(hits.keys()))
        if hits:  # pragma: no cover - only used for stats
            cls._stats_client.incr(f"{cls._stats_key}.{key_prefix}.hit", len(hits))
        if misses:  # pragma: no cover - only used for stats
            cls._stats_client.incr(f"{cls._stats_key}.{key_prefix}.miss", len(misses))

        return MultiMemcacheResult(hits=hits, misses=misses)

    @classmethod
    def set_multi(
        cls,
        key_prefix: str,
        mapping: dict[str, CacheResult],
        ttl: int,
        cache_nones: bool = False,
    ) -> None:
        """Set multiple entries into memcache in a single call"""
        prefix = cls._build_prefix(key_prefix)
        parsed_mapping = {str(k): MemcacheHolder(v) for k, v in mapping.items()}
        cache_mapping = {
            k: v
            for k, v in parsed_mapping.items()
            if cls._is_valid_cache_value(v, cache_nones=cache_nones)
        }
        if cache_mapping:  # pragma: no cover - only used for stats
            cls._stats_client.incr(f"{cls._stats_key}.{key_prefix}.set", count=len(cache_mapping))
        with cls._cache_command_stats_timer("set_multi"):
            failed_keys = cls._cache_client.set_multi(
                cache_mapping, key_prefix=prefix, ttl=cls._add_jitter(ttl)
            )
        # Extend the failed keys by any key that was filtered out by the `cache_mapping`
        failed_keys.extend(list(set(parsed_mapping.keys()) - set(cache_mapping.keys())))
        return failed_keys

    @classmethod
    def _build_prefix(cls, key_prefix: str) -> str:
        version_prefix = cls._service_version.replace(".", "-")
        return f"memcache_{version_prefix}_{key_prefix}".replace(" ", "+")

    @classmethod
    def _add_jitter(cls, ttl: int) -> int:
        """Add a percentage "jitter" to the given TTL to avoid thundering herd"""
        return int(random.uniform(ttl * 0.9, ttl * 1.1))

    @classmethod
    def _extract_mapping(
        cls, mapping: dict[str, MemcacheHolder], cache_nones: bool = False
    ) -> dict[str, CacheResult]:
        """
        Extract the value out of the `MemcacheHolder` for a given mapping dict
        (returned by the `get_multi` function)
        """
        new_mapping: dict[str, CacheResult] = {}
        for k, v in mapping.items():
            valid = cls._is_valid_cache_value(v, cache_nones=cache_nones)
            if valid:
                new_mapping[k] = v.value
        return new_mapping

    @classmethod
    def _is_valid_cache_value(cls, holder: Any, cache_nones: bool = False) -> bool:
        """
        Check whether a given item is a `MemcacheHolder` and its inner `value` is valid
        """
        if isinstance(holder, MemcacheHolder):
            value = holder.value
            if cache_nones or value is not None:
                return True
        return False

    @classmethod
    def _cache_command_stats_timer(
        cls,
        cache_command: Literal["get", "get_multi", "add", "set_multi"],
    ) -> AbstractContextManager[None]:
        return cls._stats_client.timer(f"{cls._stats_key}.commands.{cache_command}.timing")
