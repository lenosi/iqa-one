from abc import ABC, abstractmethod
from enum import Enum

from iqa.system.executor import Executor, Execution


class ServiceStatus(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'
    FAILED = 'failed'
    UNKNOWN = 'unknown'


class Service(ABC):
    """
    Represents a service used to control a Server component (Router or Broker).
    """

    TIMEOUT = 30

    def __init__(self, name: str, executor: Executor):
        self.name = name
        self.executor = executor

    @abstractmethod
    def status(self) -> ServiceStatus:
        """
        Returns the service status
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        return NotImplemented

    @abstractmethod
    def start(self, wait_for_messaging=False) -> Execution:
        return NotImplemented

    @abstractmethod
    def stop(self) -> Execution:
        return NotImplemented

    @abstractmethod
    def restart(self, wait_for_messaging=False) -> Execution:
        return NotImplemented

    @abstractmethod
    def enable(self) -> Execution:
        return NotImplemented

    @abstractmethod
    def disable(self) -> Execution:
        return NotImplemented
