from dataclasses import dataclass
from typing import NamedTuple

import pytest

from sponsored_ads_service.utils.hash import _HashedTuple

pytestmark = pytest.mark.utils


class HashkeyParams(NamedTuple):
    args: list
    kwargs: dict
    expected: any


@dataclass(frozen=True)
class HashableValue:
    a: int


@dataclass
class NonHashableValue:
    a: int

    def __repr__(self):
        return f"TEST: a={self.a}"


def func_for_test(a, b, c=1):
    return 10


class ClassForTest:
    def instance_func_for_test(self, a, b, c=1):
        return 10

    @classmethod
    def class_func_for_test(cls, a, b, c=1):
        return 10


def test_hashfunc(mocker):
    from sponsored_ads_service.utils.hash import HashUtils

    call_kwargs = {"a": 1, "b": 2, "c": 3}
    key = _HashedTuple(
        (("a", 1), ("b", 2), ("c", 3)),
    )
    mock_get_call_kwargs = mocker.patch.object(
        HashUtils, "_extract_kwargs_from_call", return_value=call_kwargs
    )
    mock_hashkey_call = mocker.patch.object(HashUtils, "hashkey", return_value=key)
    output = HashUtils.hashfunc(func_for_test, 1, 2, c=3)
    mock_get_call_kwargs.assert_called_with(func_for_test, 1, 2, c=3)
    mock_hashkey_call.assert_called_with(**call_kwargs)
    assert output == key


@pytest.mark.parametrize(
    ("args", "kwargs", "expected"),
    [
        HashkeyParams(args=[1, 2], kwargs={}, expected=_HashedTuple((1, 2))),
        HashkeyParams(
            args=[{"c": [0, 1, 2]}],
            kwargs={},
            expected=_HashedTuple(
                (frozenset({("c", (0, 1, 2))}),),
            ),
        ),
        HashkeyParams(
            args=[1],
            kwargs={"c": 3, "d": (1, 2, 3)},
            expected=_HashedTuple(
                (
                    1,
                    ("c", 3),
                    ("d", (1, 2, 3)),
                ),
            ),
        ),
        HashkeyParams(
            args=[],
            kwargs={"e": "test"},
            expected=_HashedTuple(
                (("e", "test"),),
            ),
        ),
        HashkeyParams(
            args=[1, 2],
            kwargs={"f": {"a": {1}, "b": ["val-1", "val-2"]}},
            expected=_HashedTuple(
                (
                    1,
                    2,
                    ("f", frozenset({("a", (1,)), ("b", ("val-1", "val-2"))})),
                )
            ),
        ),
        HashkeyParams(
            args=[HashableValue(10)],
            kwargs={},
            expected=_HashedTuple(
                (HashableValue(10),),
            ),
        ),
        HashkeyParams(
            args=[NonHashableValue(10)],
            kwargs={},
            expected=_HashedTuple(
                (("NonHashableValue", frozenset({("a", 10)})),),
            ),
        ),
    ],
)
def test_hashkey(args, kwargs, expected):
    from sponsored_ads_service.utils.hash import HashUtils

    output = HashUtils.hashkey(*args, **kwargs)
    assert output == expected


@pytest.mark.parametrize(
    "func",
    [
        func_for_test,
        ClassForTest().instance_func_for_test,
        ClassForTest.class_func_for_test,
    ],
)
@pytest.mark.parametrize(
    ("args", "kwargs", "expected"),
    [
        ([1, 2, 3], {}, {"a": 1, "b": 2, "c": 3}),
        ([1, 2], {}, {"a": 1, "b": 2, "c": 1}),
        ([1], {"b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3}),
    ],
)
def test_extract_kwargs_from_call(func, args, kwargs, expected):
    from sponsored_ads_service.utils.hash import HashUtils

    output = HashUtils._extract_kwargs_from_call(func, *args, **kwargs)
    assert output == expected


def test_hashed_tuple():
    from sponsored_ads_service.utils.hash import _HashedTuple

    item = _HashedTuple((1, 2, 3))
    assert item._hashvalue is None
    hash(item)
    prev = item._hashvalue
    assert prev is not None
    hash(item)
    assert item._hashvalue == prev
