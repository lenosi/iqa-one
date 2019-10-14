from typing import List

from iqa.components.abstract.component import Component
from iqa.components.abstract.configuration import Configuration
from iqa.components.abstract.management.client import ManagementClient
from iqa.abstract.listener import Listener
from iqa.system.node.node import Node
from iqa.system.service.service import Service


class ServerComponent(Component):
    """
    Super class for all Server component implementations (for now Routers and Brokers).
    """

    def __init__(self, name: str, node: Node, service: Service, listeners: List[Listener],
                 configuration: Configuration = None):
        super(ServerComponent, self).__init__(name, node)
        self.service = service
        self.name = name
        self.node = node
        self.configuration = configuration
        self.listeners = listeners
        self.management_client = self.get_management_client()

    def get_management_client(self):
        raise NotImplementedError

    @property
    def implementation(self):
        raise NotImplementedError
