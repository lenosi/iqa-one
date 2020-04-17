"""
Represents a generic Queue entity.
"""
from iqa.abstract.destination.address import Address
from iqa.abstract.destination.routing_type import RoutingType


class Queue:
    def __init__(self, name: str, routing_type: RoutingType, address: Address) -> None:
        self.name: str = name
        self.routing_type: RoutingType = routing_type
        self.address: Address = address
        self.message_count: int = 0

    @property
    def fqqn(self) -> str:
        return "%s::%s" % (self.address.name, self.name)
