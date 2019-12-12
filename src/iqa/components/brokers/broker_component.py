from iqa.abstract.server.broker import Broker
from iqa.components.abstract.server.server_component import ServerComponent
from iqa.system.node.node import Node


class BrokerComponent(ServerComponent, Broker):
    def __init__(self, name: str, node: Node, **kwargs) -> None:
        super(BrokerComponent, self).__init__(name, node, **kwargs)
