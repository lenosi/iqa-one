"""
Represents a generic Queue entity.
"""
from iqa.abstract.destination import Address
from iqa.abstract.destination import RoutingType


class Queue:
    def __init__(self, name: str, routing_type: RoutingType, address: Address):
        self.name = name
        self.routing_type = routing_type
        self.address = address
        self.message_count = None

    @property
    def fqqn(self):
        return "%s::%s" % (self.address.name, self.name)
