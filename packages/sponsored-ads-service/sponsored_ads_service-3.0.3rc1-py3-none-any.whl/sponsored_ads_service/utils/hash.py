"""
TODO: This version of creating keys from parameters has bugs. This needs to be updated
to be in line with the more recent versions.
"""

from __future__ import annotations

import inspect
import logging
from collections.abc import Callable, Hashable
from typing import Any

logger = logging.getLogger(__name__)


class HashUtils:
    """A utility class for creating hashable cache keys"""

    @classmethod
    def hashfunc(cls, func: Callable, *args: Any, **kwargs: Any) -> _HashedTuple:
        """Create a hashable key for a given function call"""
        call_kwargs = cls._extract_kwargs_from_call(func, *args, **kwargs)
        return cls.hashkey(**call_kwargs)

    @classmethod
    def hashkey(cls, *args: Any, **kwargs: Any) -> _HashedTuple:
        """Create a hashable key for a given set of arguments and keyword arguments"""
        key_parts = [cls._get_hashable_value(v) for v in args]
        if kwargs:
            key_parts.extend([cls._get_hashable_value([k, v]) for k, v in kwargs.items()])
        return _HashedTuple(key_parts)

    @classmethod
    def _get_hashable_value(cls, value: Any) -> Any:  # pragma: no cover
        # TODO: This is borked and needs rewriting
        """Get a hashable version of `value`"""
        if isinstance(value, (dict | list | set | tuple)):
            return cls._freeze(value)
        if isinstance(value, Hashable):
            return value
        if hasattr(value, "__dict__") and hasattr(value, "__class__"):
            return cls._freeze(value)
        return str(value)

    @classmethod
    def _freeze(cls, o: Any) -> Any:
        """Provide a frozen (hashable) equivalent of a given object `o`"""
        if hasattr(o, "__dict__") and hasattr(o, "__class__"):
            return cls._freeze([o.__class__.__name__, o.__dict__])
        if isinstance(o, dict):
            return frozenset([(k, cls._freeze(v)) for k, v in o.items()])
        if isinstance(o, set):
            return tuple(sorted(cls._freeze(v) for v in o))
        if isinstance(o, (list | tuple)):
            return tuple([cls._freeze(v) for v in o])
        return o

    @classmethod
    def _extract_kwargs_from_call(
        cls, func: Callable, *args: Any, **kwargs: Any
    ) -> dict[str, Any]:
        """
        Extract a kwargs dict from a function call, this will convert args into kwargs
        """
        bound_sig = inspect.signature(func).bind(*args, **kwargs)
        bound_sig.apply_defaults()
        call_kwargs = bound_sig.arguments
        for k in ["self", "cls"]:
            call_kwargs.pop(k, None)
        return call_kwargs


class _HashedTuple(tuple):
    """
    A tuple that ensures that hash() will be called no more than once
    per element, since cache decorators will hash the key multiple
    times on a cache miss.  See also _HashedSeq in the standard
    library functools implementation.
    """

    _hashvalue = None

    def __hash__(self) -> int:
        hashvalue = self._hashvalue
        if hashvalue is None:
            self._hashvalue = hashvalue = super().__hash__()
        return hashvalue
