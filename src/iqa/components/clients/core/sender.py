from iqa.components.clients.core.client import CoreMessagingClient
from iqa.abstract.client.sender import Sender
from iqa.system.node.node import Node


class SenderCore(CoreMessagingClient, Sender):
    """Core python sender client."""

    def __init__(self, name: str, node: Node):
        super().__init__(name, node)
        #  TODO - Define what kind of object the core sender is going to use (maybe the default for python ext. client)
