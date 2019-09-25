from abc import ABC, abstractmethod

from iqa.abstract.listener import Listener


class Client(ABC):
    """
    Abstract class for every abstract client
    """

    def __init__(self, **kwargs):
        self.url = None  # connectionUrl
        self.users = None
        self.logs = None

    @property
    @abstractmethod
    def name(self):
        """

        :return: String
        """
        pass

    @property
    @abstractmethod
    def version(self):
        """

        :return: String
        """
        pass

    @property
    @abstractmethod
    def supported_protocols(self):
        """

        :return: List
        """
        pass

    @abstractmethod
    def set_url(self, url: str):
        pass

    @abstractmethod
    def set_endpoint(self, listener: Listener):
        pass

    @abstractmethod
    def connect(self):
        """
        Create connection to the endpoint
        :return:
        :rtype:
        """
        pass
