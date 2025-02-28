"""
Some helper types used for creating decorators (since the `Callable` types
can get quite lengthy to do manually).
```
    def decorator(a: int) -> DecoratedWithArgs:
        def wrapper(func: Decorated) -> Decorated:
            @wraps(func)
            def inner(*args: Any, **kwargs: Any) -> DecoratedReturnType:
                return func(*args, **kwargs)
            return inner
        return wrapper
```
"""

from collections.abc import Callable
from typing import TypeVar

DecoratedReturnType = TypeVar("DecoratedReturnType")

Decorated = Callable[..., DecoratedReturnType]

DecoratedWithArgs = Callable[[Decorated], Decorated]
