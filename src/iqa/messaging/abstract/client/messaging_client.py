from abc import ABC, abstractmethod

from iqa.messaging.abstract.client import Client
from iqa.messaging.abstract.listener import Listener


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
        :rtype: iqa.iqa.messaging.abstract.message.Message
        """
        return self.messages[-1] if self.messages else None
