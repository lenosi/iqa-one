import pytest
from iqa.utils.utils import get_subclasses


class SomeClass:
    some_property: str = 'ABC'


class SomeClassParent1(SomeClass):
    some_property: str = 'Parent1'


class SomeClassParent2(SomeClass):
    some_property: str = 'Parent2'


def test_get_subclasses_property():
    cls = get_subclasses(given_name='Parent1', in_class=SomeClass, in_class_property='some_property')
    assert cls.some_property == 'Parent1'


def test_get_subclasses_name():
    cls = get_subclasses(given_name='SomeClassParent2', in_class=SomeClass)
    assert cls.some_property == 'Parent2'


def test_get_subclasses_fail():
    with pytest.raises(ValueError, match=r".* not found as a subclasses .*"):
        cls = get_subclasses(given_name='SomeClassParent3', in_class=SomeClass)
        cls()


def test_get_subclasses_property_fail():
    with pytest.raises(AttributeError, match=r".* has no attribute .*"):
        cls = get_subclasses(given_name='SomeClassParent2', in_class=SomeClass, in_class_property='none_property')
        cls()
