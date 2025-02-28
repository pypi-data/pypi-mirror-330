from dataclasses import dataclass
from typing import Generic, TypeVar

CacheResult = TypeVar("CacheResult")


@dataclass(frozen=True)
class MemcacheHolder(Generic[CacheResult]):
    """
    This is a simple wrapper around the `CacheResult` that allows us to cache `None`.
    This should only be used interally within `MemcacheUtils`
    """

    value: CacheResult


@dataclass(frozen=True)
class MultiMemcacheResult(Generic[CacheResult]):
    """
    The results from a memcache `get_multi` containing the cache hits, and keys that
    were cache misses
    """

    hits: dict[str, CacheResult]
    misses: list[str]
