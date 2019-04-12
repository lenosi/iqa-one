from abc import ABC, abstractmethod

from iqa.messaging.abstract.listener import Listener


class MessagingServer(ABC):

    def __init__(self) -> None:
        self.listeners = None
        self.connectors = None

    @property
    def get_listeners(self) -> list(Listener):
        return self.listeners

    @abstractmethod
    def get_url(self, port: int = None, listener: Listener = None) -> str:
        pass

    @abstractmethod
    def get_urls(self, schema: str) -> list(Listener):
        pass

