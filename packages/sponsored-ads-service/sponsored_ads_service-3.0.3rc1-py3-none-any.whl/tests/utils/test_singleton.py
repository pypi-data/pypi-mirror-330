import pytest

pytestmark = pytest.mark.utils


@pytest.fixture
def singleton():
    """Override default fixture for `singleton` (and wipe the mapping between tests)"""
    from sponsored_ads_service.utils.singleton import SingletonMeta

    SingletonMeta._SingletonMeta__instances = {}


def test_singleton():
    from sponsored_ads_service.utils.singleton import SingletonMeta

    class TestClassA(metaclass=SingletonMeta): ...

    class TestClassB(metaclass=SingletonMeta): ...

    a1 = TestClassA()
    a2 = TestClassA()

    b1 = TestClassB()
    b2 = TestClassB()

    assert id(a1) == id(a2)
    assert id(b1) == id(b2)
    # Ensure that instances of the same class share the same lock (class level)
    assert a1.__shared_instance_lock__ == a2.__shared_instance_lock__

    assert id(a1) != id(b1)
    # Ensure that each class has its own instance lock
    assert TestClassA.__shared_instance_lock__ != TestClassB.__shared_instance_lock__


def test_singleton_no_deadlock():
    from sponsored_ads_service.utils.singleton import SingletonMeta

    class TestClassInner(metaclass=SingletonMeta): ...

    class TestClass(metaclass=SingletonMeta):
        def __init__(self) -> None:
            self.inner = TestClassInner()

    c1 = TestClass()
    c2 = TestClass()

    assert id(c1) == id(c2)
    assert id(c1.inner) == id(c2.inner)

    inner = TestClassInner()
    assert id(c1.inner) == id(inner)
