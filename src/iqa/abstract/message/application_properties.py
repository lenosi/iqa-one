from dataclasses import dataclass
from typing import Optional


# noinspection PyDunderSlots
@dataclass(frozen=False)
class Property:
    """
    The keys of this map are restricted to be of type string (which excludes the possibility of a null key)
    and the values are restricted to be of simple types only, that is, excluding map, list, and array types.
    """

    def __init__(self, name: str, value: Optional[str] = None) -> None:
        self.name: str = name
        self.value: Optional[str] = value


class ApplicationProperties(list):
    """
    The application-properties section is a part of the bare message used for structured application data.
    Intermediaries can use the data within this structure for the purposes of filtering or routing.

    """

    def add_property(self, name: str, value: str) -> None:
        """
        Add property to message Application properties
        :param name:
        :param value:
        :return:
        """
        self.append(Property(name=name, value=value))
