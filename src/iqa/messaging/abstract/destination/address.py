from typing import List

from iqa.messaging.abstract.destination.routing_type import RoutingType


class Address:
    """
    Address class
    """

    def __init__(self, name: str, routing_type: RoutingType):
        self.name = name
        self.routing_type = routing_type
        self._queues: List = list()

    @property
    def queues(self) -> List:
        return self._queues
