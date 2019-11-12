from iqa.components.clients.core.client import CoreMessagingClient
from iqa.abstract.client import Receiver
from iqa.system.node import Node, Executor


class ReceiverCore(Receiver, CoreMessagingClient):
    """Core python receiver client."""

    def __init__(self, name: str, node: Node, executor: Executor) -> None:
        super(ReceiverCore, self).__init__(name, node, executor)
        #  TODO - Define what kind of object the core receiver is
        #   going to use (maybe the default for python ext. client)
