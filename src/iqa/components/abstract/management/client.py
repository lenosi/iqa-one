import abc
from abc import ABC

from iqa.abstract.destination.destination import Destination


class ManagementClient(ABC):

    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def create_destination(self, destination: Destination) -> Destination:
        """
        Creates an address using its name and specialized type (ANYCAST, MULTICAST).
        :param destination:
        :return:
        """
        pass

    @abc.abstractmethod
    def delete_destination(self, name: str, remove_consumers: bool = False) -> None:
        """
        Deletes a given destination.
        :param name:
        :param remove_consumers:
        :return:
        """
        pass
