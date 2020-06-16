from abc import ABC, abstractmethod

from iqa.logger import logger


class ConnectionBase(ABC):
    """ Abstract IO Connection Interface """

    def __init__(self, host, port, **kwargs) -> None:
        self._logger = logger
        self._host: str = host
        self._port: int = port

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
