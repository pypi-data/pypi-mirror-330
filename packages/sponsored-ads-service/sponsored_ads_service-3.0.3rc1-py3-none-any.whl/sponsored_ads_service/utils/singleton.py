from __future__ import annotations

from threading import Lock
from typing import Any, ClassVar, cast


class SingletonMeta(type):
    """
    Turn the given class into a singleton by using this metaclass.
    Usage:
    ```
    class SomeClass(metaclass=SingletonMeta):
        ...
    ```
    """

    __instances: ClassVar[dict] = {}
    __shared_instance_lock__: Lock

    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> SingletonMeta:
        singleton_meta = cast(SingletonMeta, super().__new__(cls, name, bases, attrs))
        singleton_meta.__shared_instance_lock__ = Lock()
        return cast(SingletonMeta, singleton_meta)

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        # Use double checked locking (check-lock-check) for performance improvements
        # See: https://en.wikipedia.org/wiki/Double-checked_locking
        if cls not in cls.__instances:
            with cls.__shared_instance_lock__:
                if cls not in cls.__instances:  # pragma: no cover
                    cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]
