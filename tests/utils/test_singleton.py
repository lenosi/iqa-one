from unittest import TestCase

from iqa.utils.singleton import Singleton, SingletonMeta


@Singleton
class FooSingletonDecorator:
    def __init__(self):
        self.value = True


class TestSingleton(TestCase):
    def test_instance(self):
        assert FooSingletonDecorator.Instance().value

    def test_failure(self):
        with self.assertRaises(Exception) as context:
            FooSingletonDecorator()

        self.assertTrue('Singletons must be accessed through `Instance()`.' in str(context.exception))


class FooSingletonMeta(metaclass=SingletonMeta):
    def __init__(self):
        self.value = True


class TestSingletonMeta(TestCase):
    def test_instance(self):
        foo = FooSingletonMeta()
        assert foo.value
