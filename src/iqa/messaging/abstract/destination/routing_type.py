from enum import Enum, auto


class RoutingType(Enum):
    """
    Routing type
    """
    ANYCAST = auto()
    MULTICAST = auto()
    BOTH = auto()

    @staticmethod
    def from_value(value: str):
        if not value:
            return RoutingType.ANYCAST

        if value.__contains__('ANYCAST') and value.__contains__('MULTICAST'):
            return RoutingType.BOTH
        elif value.__contains__('ANYCAST'):
            return RoutingType.ANYCAST
        elif value.__contains__('MULTICAST'):
            return RoutingType.MULTICAST
        else:
            # If some unexpected value, then return both
            return RoutingType.BOTH
