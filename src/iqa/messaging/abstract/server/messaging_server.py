from abc import ABC, abstractmethod

from iqa.messaging.abstract.listener import Listener


class MessagingServer(ABC):
    implementation = NotImplemented

    def __init__(self) -> None:
        self.listeners = []
        self.connectors = []

    @abstractmethod
    def get_url(self, port: int = None, listener: Listener = None) -> str:
        return NotImplemented
