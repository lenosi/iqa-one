from abc import ABC
from typing import Optional, Any


class Protocol(ABC):
    """Protocol abstraction"""

    name: str = NotImplementedError
    default_port: Optional[int] = NotImplementedError
    transport: Any = NotImplementedError

