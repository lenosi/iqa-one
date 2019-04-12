from enum import Enum

from iqa.system.executor import Executor, Execution


class ServiceStatus(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'
    FAILED = 'failed'
    UNKNOWN = 'unknown'


class Service(object):
    """
    Represents a service used to control a Server component (Router or Broker).
    """

    TIMEOUT = 30

    def __init__(self, name: str, executor: Executor):
        self.name = name
        self.executor = executor

    def status(self) -> ServiceStatus:
        """
        Returns the service status
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        raise NotImplementedError()

    def start(self, wait_for_messaging=False) -> Execution:
        raise NotImplementedError()

    def stop(self) -> Execution:
        raise NotImplementedError()

    def restart(self, wait_for_messaging=False) -> Execution:
        raise NotImplementedError()

    def enable(self) -> Execution:
        raise NotImplementedError()

    def disable(self) -> Execution:
        raise NotImplementedError()
