from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from iqa.system.executor import Executor
from iqa.system.executor.execution import Execution


class ServiceStatus(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'
    FAILED = 'failed'
    UNKNOWN = 'unknown'


class Service(ABC):
    """
    Represents a service used to control a Server component (Router or Broker).
    """

    TIMEOUT: int = 30

    def __init__(self, name: Optional[str], executor: Executor) -> None:
        self.name: Optional[str] = name
        self.executor: Executor = executor

    @abstractmethod
    def status(self) -> ServiceStatus:
        """
        Returns the service status
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        return NotImplemented

    @abstractmethod
    def start(self) -> Execution:
        return NotImplemented

    @abstractmethod
    def stop(self) -> Execution:
        return NotImplemented

    @abstractmethod
    def restart(self) -> Execution:
        return NotImplemented

    @abstractmethod
    def enable(self) -> Optional[Execution]:
        return NotImplemented

    @abstractmethod
    def disable(self) -> Optional[Execution]:
        return NotImplemented
