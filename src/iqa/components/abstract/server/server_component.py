from typing import List, Optional

from iqa.components.abstract.component import Component
from iqa.components.abstract.configuration import Configuration
from iqa.abstract.listener import Listener
from iqa.system.node.node import Node
from iqa.system.service.service import Service
from iqa.utils.types import ManagementClientType


class ServerComponent(Component):
    """
    Super class for all Server component implementations (for now Routers and Brokers).
    """

    def __init__(self, name: str, node: Node, service: Service, listeners: List[Listener],
                 configuration: Configuration = None) -> None:
        super(ServerComponent, self).__init__(name, node)
        self.service: Service = service
        self.name: str = name
        self.node: Node = node
        self.configuration: Optional[Configuration] = configuration
        self.listeners: List[Listener] = listeners
        self.management_client: ManagementClientType = self.get_management_client()

    def get_management_client(self) -> ManagementClientType:
        raise NotImplementedError

    @property
    def implementation(self):
        raise NotImplementedError
