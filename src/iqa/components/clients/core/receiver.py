from iqa.components.clients.core.client import CoreMessagingClient
from iqa.abstract.client.receiver import Receiver
from iqa.system.node.node import Node


class ReceiverCore(CoreMessagingClient, Receiver):
    """Core python receiver client."""

    def __init__(self, name: str, node: Node) -> None:
        super(ReceiverCore, self).__init__(name, node)
        #  TODO - Define what kind of object the core receiver is
        #   going to use (maybe the default for python ext. client)
