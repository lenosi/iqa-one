import abc
from abc import ABC

from iqa.messaging.abstract.destination.destination import Destination


class ManagementClient(ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def create_destination(self, destination: Destination):
        """
        Creates an address using its name and specialized type (ANYCAST, MULTICAST).
        :param address:
        :return:
        """
        pass

    @abc.abstractmethod
    def delete_destination(self, name: str, remove_consumers: bool = False):
        """
        Deletes a given destination.
        :param name:
        :param remove_consumers:
        :return:
        """
        pass
