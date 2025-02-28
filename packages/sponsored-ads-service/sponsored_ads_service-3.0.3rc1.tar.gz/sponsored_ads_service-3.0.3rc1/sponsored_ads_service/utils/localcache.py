"""
TODO: Rewrite to allow dependency injection and lazy fetching of cache classes.

```python
class SomeClass:
    def __init__(self):
        self._some_func_localcache = TTLCache(ttl=100, maxsize=600)

    @localcached_method("prefix", cache=lambda self: self._some_func_localcache)
    def some_func(self, a: int) -> int:
        ...
```
"""

import logging
from functools import wraps
from typing import Any, cast

from cachetools import Cache, TTLCache
from opentelemetry import trace

from sponsored_ads_service.configuration import Clients, SponsoredAdsConfig
from sponsored_ads_service.errors import ConfigurationError
from sponsored_ads_service.models.caching import CacheResult
from sponsored_ads_service.models.decorated import Decorated, DecoratedWithArgs

from .hash import HashUtils

__all__ = ["LocalcacheUtils"]

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class LocalcacheUtils:
    """A utility class for integrating with local caches"""

    _localcache_enabled = SponsoredAdsConfig().get_localcache_enabled()
    _stats_client = Clients().stats_client

    @classmethod
    def cached_from_config(cls, context: str) -> DecoratedWithArgs:
        if not context.isidentifier():
            # isidentifier gives us a good enough test, we mainly want to prevent dashes
            raise ConfigurationError(
                "Invalid localcache key for config, only use keys that can be valid "
                f"unix environment variables: '{context}'"
            )

        cache_config = SponsoredAdsConfig().get_localcache_context(context)

        return cls.cached(
            ttl=cache_config.ttl,
            maxsize=cache_config.maxsize,
            stats_key=context,
            enabled=cache_config.enabled,
        )

    @classmethod
    def cached(
        cls,
        ttl: int,
        maxsize: int = 32,
        stats_key: str | None = None,
        enabled: bool = True,
    ) -> DecoratedWithArgs:
        """
        Cache the result of the given method locally (in memory). The `stats_key` can be
        left as `None` to use the function name

        Use it as:
        ```
            @LocalcacheUtils.cached(ttl=1200, maxsize=3)
            def function_to_cache(p1, p2):
                ...
        ```
        """

        def decorator(func: Decorated[CacheResult]) -> Decorated[CacheResult]:
            cache: TTLCache = TTLCache(ttl=ttl, maxsize=maxsize)
            func._localcache = cache  # type: ignore
            stats_prefix = stats_key or func.__name__

            @wraps(func)
            def inner(*args: Any, **kwargs: Any) -> CacheResult:
                if not cls._localcache_enabled or not enabled:
                    return func(*args, **kwargs)
                key = HashUtils.hashfunc(func, *args, **kwargs)
                found, val = cls._get(cache, key, stats_key=stats_prefix)
                if found:
                    return cast(CacheResult, val)
                results = func(*args, **kwargs)
                cls._set(cache, key, results, stats_key=stats_prefix)
                return results

            return inner

        return decorator

    @classmethod
    def _get(cls, cache: Cache, key: Any, stats_key: str) -> tuple[bool, CacheResult | None]:
        """
        Gets the value for the given key from the provided cache object,
        returns as (`found`, `value`)
        """
        with tracer.start_as_current_span(
            "localcache.get", attributes={"stats_key": stats_key, "key": key}
        ) as span:
            try:  # Don't use `.get()` as then `None` is not cacheable
                result = cache[key]
                cls._stats_client.incr(f"caching.{stats_key}.hit")
                span.set_attribute("cache.hit", True)
                return True, result
            except KeyError:
                cls._stats_client.incr(f"caching.{stats_key}.miss")
                span.set_attribute("cache.hit", False)
                return False, None

    @classmethod
    def _set(cls, cache: Cache, key: Any, value: CacheResult, stats_key: str) -> bool:
        """Set a value for the given key in the provided cache object"""
        with tracer.start_as_current_span(
            "localcache.set", attributes={"stats_key": stats_key, "key": key}
        ):
            try:
                cache[key] = value
                cls._stats_client.incr(f"caching.localcache.{stats_key}.set")
                return True
            except Exception:  # Don't error out wrapped code if set fails
                return False
