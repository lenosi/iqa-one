from abc import ABC, abstractmethod
from typing import List, Optional

from iqa.abstract.listener import Listener


class MessagingServer(ABC):
    implementation = NotImplemented

    def __init__(self) -> None:
        self.listeners: Optional[List[Listener]] = []
        self.connectors: list = []

    @abstractmethod
    def get_url(self, port: int = None, listener: Listener = None) -> str:
        return NotImplemented
