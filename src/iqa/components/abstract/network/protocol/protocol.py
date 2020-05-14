from abc import ABC, abstractmethod
from typing import Any


class Protocol(ABC):
    """Protocol abstraction"""

    @abstractmethod
    @property
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    @property
    def default_port(self) -> int:
        raise NotImplementedError

    @abstractmethod
    @property
    def transport(self) -> Any:
        raise NotImplementedError
