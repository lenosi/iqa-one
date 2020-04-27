from abc import ABC, abstractmethod
from typing import Optional

from iqa.abstract.listener import Listener


class Client(ABC):
    """
    Abstract class for every abstract client
    """

    def __init__(self) -> None:
        self.url = None  # connectionUrl
        self.users = None
        self.logs = None

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """

        :return: String
        """

    @property
    @abstractmethod
    def version(self) -> Optional[str]:
        """

        :return: String
        """

    @property
    @abstractmethod
    def supported_protocols(self) -> list:
        """

        :return: List
        """

    @abstractmethod
    def set_url(self, url: str) -> None:
        pass

    @abstractmethod
    def set_endpoint(self, listener: Listener) -> None:
        pass

    @abstractmethod
    def connect(self):
        """
        Create connection to the endpoint
        :return:
        :rtype:
        """

    @property
    def implementation(self):
        return NotImplementedError
