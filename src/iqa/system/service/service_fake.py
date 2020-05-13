import abc
from typing import Optional

from iqa.system.executor import Executor
from iqa.system.executor import Execution
from .service import Service, ServiceStatus


class ServiceFake(Service):
    """
    Represents a service used to control a Server component (Router or Broker).
    """

    TIMEOUT: int = 30

    def __init__(self, name: Optional[str], executor: Executor):
        super().__init__(name, executor)
        self.name: Optional[str] = name
        self.executor: Executor = executor

    @abc.abstractmethod
    def status(self) -> ServiceStatus:
        """
        Returns the service status
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        return NotImplemented

    @abc.abstractmethod
    def start(self, wait_for_messaging: bool = False) -> Execution:
        return NotImplemented

    @abc.abstractmethod
    def stop(self) -> Execution:
        return NotImplemented

    @abc.abstractmethod
    def restart(self, wait_for_messaging: bool = False) -> Execution:
        return NotImplemented

    @abc.abstractmethod
    def enable(self) -> Execution:
        return NotImplemented

    @abc.abstractmethod
    def disable(self) -> Execution:
        return NotImplemented
