from abc import abstractmethod

from iqa.abstract.client import Client
from iqa.abstract.listener import Listener


class MessagingClient(Client):
    """
    Abstract class for every abstract messaging client
    """

    # Required variables
    supported_protocols = []
    name = None
    version = None

    def __init__(self, name: str, **kwargs):
        super(MessagingClient).__init__(name, **kwargs)
        self.message_buffer = None  # type: bool
        self.messages = []  # type: list
        self.message_counter = 0  # type: int

    @property
    def last_message(self):
        """Method for pickup last received message.
        :return: Last message received or None
        :rtype: iqa.iqa.abstract.message.Message
        """
        return self.messages[-1] if self.messages else None

    @abstractmethod
    def set_endpoint(self, listener: Listener):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def set_url(self, url: str):
        pass
