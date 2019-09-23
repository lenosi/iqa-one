import abc

from iqa.components.abstract.management.client import ManagementClient
from iqa.messaging.abstract.destination.address import Address
from iqa.messaging.abstract.destination.destination import Destination
from iqa.messaging.abstract.destination.queue import Queue


class ManagementBroker(ManagementClient):

    def __init__(self):
        super(ManagementBroker).__init__()

    def create_destination(self, destination: Destination):  # Address
        pass

    def delete_destination(self, name: str, remove_consumers: bool = False):  # Address
        pass

    @abc.abstractmethod
    def create_address(self, address: Address):
        """
        Creates an address using its name and specialized type (ANYCAST, MULTICAST).
        :param address:
        :return:
        """
        pass

    @abc.abstractmethod
    def create_queue(self, queue: Queue, address: Address, durable: bool = True):
        """
        Creates a queue using its name and specialized type, nested to the given address.
        :param queue:
        :param address:
        :param durable:
        :return:
        """

    @abc.abstractmethod
    def delete_address(self, name: str, force: bool = False):
        """
        Deletes a given address.
        :param name:
        :param force:
        :return:
        """
        pass

    @abc.abstractmethod
    def delete_queue(self, name: str, remove_consumers: bool = False):
        """
        Deletes a given queue.
        :param name:
        :param remove_consumers:
        :return:
        """
        pass
