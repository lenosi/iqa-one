from abc import abstractmethod

from iqa.abstract.client import MessagingClient


class Receiver(MessagingClient):
    """Abstract class of client's receivers."""

    def __init__(self, message_buffer=True, **kwargs):
        super(Receiver, self).__init__(**kwargs)
        # Sender settings

    def receive(self):
        """Method for receive message.
        :param message: Received message to be stored
        :type message: iqa.iqa.abstract.message.Message
        """
        recv_messages = self._receive()
        if self.message_buffer:
            self.messages.extend(recv_messages)  # multiple Messages

        self.message_counter += len(recv_messages)

    @abstractmethod
    def _receive(self):
        raise NotImplementedError
