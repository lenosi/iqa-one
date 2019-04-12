from abc import ABC, abstractmethod

from iqa.messaging.abstract.listener import Listener


class Client(ABC):
    """
    Abstract class for every abstract client
    """

    # Required variables
    supported_protocols = []
    name = None
    version = None

    def __init__(self, name: str, **kwargs):
        self.url = None  # connectionUrl
        self.users = None
        self.logs = None

    @abstractmethod
    def set_url(self, url: str):
        pass

    @abstractmethod
    def set_endpoint(self, listener : Listener):
        pass


    @abstractmethod
    def connect(self):
        """
        Create connection to the endpoint
        :return:
        :rtype:
        """
        pass
