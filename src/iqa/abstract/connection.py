from abc import ABC, abstractmethod


class ConnectionBase(ABC):
    """ Abstract IO Connection Interface """

    @abstractmethod
    async def disconnect(self) -> None:
        """ Close connection """
        pass

    @abstractmethod
    async def connect(self) -> None:
        """ Establish connection """
        pass

    @property
    @abstractmethod
    def host(self) -> str:
        """ Return the host address """
        pass
