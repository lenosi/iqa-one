from abc import ABC, abstractmethod

from iqa.abstract.listener import Listener


class MessagingServer(ABC):
    implementation = NotImplemented

    def __init__(self) -> None:
        self.listeners: list = []
        self.connectors: list = []

    @abstractmethod
    def get_url(self, port: int = None, listener: Listener = None) -> str:
        return NotImplemented
