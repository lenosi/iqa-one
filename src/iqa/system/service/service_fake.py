import abc
from enum import Enum

from iqa.system.executor import Executor, Execution
from .service import Service


class ServiceStatus(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'
    FAILED = 'failed'
    UNKNOWN = 'unknown'


class ServiceFake(Service):
    """
    Represents a service used to control a Server component (Router or Broker).
    """

    TIMEOUT = 30

    def __init__(self, name: str, executor: Executor):
        super().__init__(name, executor)
        self.name = name
        self.executor = executor

    @abc.abstractmethod
    def status(self) -> ServiceStatus:
        """
        Returns the service status
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def start(self, wait_for_messaging=False) -> Execution:
        raise NotImplementedError()

    @abc.abstractmethod
    def stop(self) -> Execution:
        raise NotImplementedError()

    @abc.abstractmethod
    def restart(self, wait_for_messaging=False) -> Execution:
        raise NotImplementedError()

    @abc.abstractmethod
    def enable(self) -> Execution:
        raise NotImplementedError()

    @abc.abstractmethod
    def disable(self) -> Execution:
        raise NotImplementedError()
