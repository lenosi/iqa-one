from enum import Enum, auto


class RoutingType(Enum):
    """
    Routing type
    """
    ANYCAST: auto = auto()
    MULTICAST: auto = auto()
    BOTH: auto = auto()

    @staticmethod
    def from_value(value: str) -> 'RoutingType':
        if not value:
            return RoutingType.ANYCAST

        if value.__contains__('ANYCAST') and value.__contains__('MULTICAST'):
            return RoutingType.BOTH
        elif value.__contains__('ANYCAST'):
            return RoutingType.ANYCAST
        elif value.__contains__('MULTICAST'):
            return RoutingType.MULTICAST
        else:
            raise ValueError('Value "%s" does not match.' % value)
