from typing import Optional
from .transport import Transport


class WebSocket(Transport):
    def __init__(self) -> None:
        Transport.__init__(self)
        self.name: Optional[str] = None
