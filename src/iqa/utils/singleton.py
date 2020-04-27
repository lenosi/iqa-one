from typing import Any


class Singleton:
    """Decorator Singleton"""

    def __init__(self, cls) -> None:
        self._cls: Any = cls

    def Instance(self) -> Any:
        try:
            return self._instance
        except AttributeError:
            self._instance: Any = self._cls()
            return self._instance

    def __call__(self) -> Any:
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst) -> Any:
        return isinstance(inst, self._cls)


class SingletonMeta(type):
    """Metaclass for Singleton classes"""

    def __init__(cls, name, bases, dictionary):
        super(SingletonMeta, cls).__init__(cls, bases, dictionary)
        cls._instanceDict = {}

    def __call__(cls, *args, **kwargs):
        argdict = {'args': args}
        argdict.update(kwargs)
        argset = frozenset(argdict)
        if argset not in cls._instanceDict:
            cls._instanceDict[argset] = super(SingletonMeta, cls).__call__(
                *args, **kwargs
            )
        return cls._instanceDict[argset]
