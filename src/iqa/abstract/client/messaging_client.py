from abc import abstractmethod
from typing import Optional

from iqa.abstract.client.client import Client
from iqa.abstract.listener import Listener
from iqa.abstract.message.message import Message


class MessagingClient(Client):
    """
    Abstract class for every abstract messaging client
    """

    # Required variables
    supported_protocols: list = []
    name: Optional[str] = None
    version: Optional[str] = None

    def __init__(self, message_buffer: bool = True) -> None:
        super(MessagingClient, self).__init__()
        self.message_buffer: bool = message_buffer
        self.messages: list = []
        self.message_counter: int = 0

    @property
    def last_message(self) -> Message:
        """Method for picking up last received message.
        :return: Last message received or None
        :rtype: iqa.iqa.abstract.message.Message
        """
        return self.messages[-1] if self.messages else None

    @abstractmethod
    def set_endpoint(self, listener: Listener) -> None:
        pass

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def set_url(self, url: str) -> None:
        pass
