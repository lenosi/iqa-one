from typing import Optional


class Protocol:
    """ Protocol abstraction"""

    default_port: Optional[int] = None

    def __init__(self, transport) -> None:
        self.name: str = type(self).__name__
        self.transport = transport
