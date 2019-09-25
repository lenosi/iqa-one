from abc import abstractmethod

from iqa.abstract.client import MessagingClient
from iqa.abstract.message import Message


class Sender(MessagingClient):
    """Abstract class of sender client."""

    def __init__(self, name: str, **kwargs):
        super(Sender, self).__init__(name, **kwargs)
        # Sender settings

    def send(self, message: Message, **kwargs):
        """Method for send message.
        :param message: Message to be sent
        :type: iqa.iqa.abstract.message.Message
        """
        if self.message_buffer:
            self.messages.append(message)  # single sent Message

        self.message_counter += 1
        self._send(message, **kwargs)

    @abstractmethod
    def _send(self, message: Message, **kwargs):
        raise NotImplementedError
