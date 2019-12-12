from iqa.components.protocols.amqp import Amqp10
from iqa.components.clients.external import ClientExternal
from iqa.system.node.node import Node


class ClientPython(ClientExternal):
    """Python Proton client (base abstract class)."""

    supported_protocols: list = [Amqp10()]
    implementation: str = 'python'
    version: str = '1.0.1'

    def __init__(self, name: str, node: Node, **kwargs) -> None:
        super(ClientPython, self).__init__(name, node, **kwargs)
