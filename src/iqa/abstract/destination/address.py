from iqa.abstract.destination.routing_type import RoutingType


class Address:
    """
    Address class
    """

    def __init__(self, name: str, routing_type: RoutingType) -> None:
        self.name: str = name
        self.routing_type: RoutingType = routing_type
        self._queues: list = list()

    @property
    def queues(self) -> list:
        return self._queues
