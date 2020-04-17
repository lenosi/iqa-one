import logging
from enum import Enum
from typing import Optional
from docker.errors import APIError, NotFound

from iqa.system.command.command_ansible import CommandAnsible
from iqa.system.command.command_base import Command
from iqa.system.executor import ExecutorAnsible, ExecutorContainer
from iqa.system.executor.execution import Execution
from iqa.system.command.command_container import CommandContainer
from iqa.system.service.service import Service, ServiceStatus
from iqa.utils.docker_util import DockerUtil


class ServiceDocker(Service):
    """
    Implementation of a service represented by a docker container.
    So startup and shutdown are done by managing current state of related
    docker container name.
    """
    _logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, name: str, executor: ExecutorContainer) -> None:
        super().__init__(name, executor)
        self.docker_host: Optional[str] = executor.docker_host
        self.docker_util: DockerUtil = DockerUtil(docker_host=executor.docker_host)

    class ServiceDockerState(Enum):
        STARTED = ('start', 'started')
        STOPPED = ('stop', 'stopped')
        RESTARTED = ('restart', 'started')

        def __init__(self, system_state, ansible_state) -> None:
            self.system_state = system_state
            self.ansible_state = ansible_state

    def status(self) -> ServiceStatus:
        """
        Returns the status based on status of container name.
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        try:
            container = self.docker_util.get_container(self.name)
            if not container:
                ServiceDocker._logger.debug("Service: %s - Status: UNKNOWN" % self.name)
                return ServiceStatus.UNKNOWN

            if container.status == 'running':
                ServiceDocker._logger.debug("Service: %s - Status: RUNNING" % self.name)
                return ServiceStatus.RUNNING
            elif container.status == 'exited':
                ServiceDocker._logger.debug("Service: %s - Status: STOPPED" % self.name)
                return ServiceStatus.STOPPED
        except APIError or NotFound:
            ServiceDocker._logger.exception('Error retrieving status of docker container')
            return ServiceStatus.FAILED

        return ServiceStatus.UNKNOWN

    def start(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceDockerState.STARTED))

    def stop(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceDockerState.STOPPED))

    def restart(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceDockerState.RESTARTED))

    def enable(self) -> Optional[Execution]:
        """
        Simply ignore it (not applicable to containers)
        :return:
        """
        return None

    def disable(self) -> Optional[Execution]:
        """
        Simply ignore it (not applicable to containers)
        :return:
        """
        return None

    def _create_command(self, service_state: ServiceDockerState) -> Command:
        """
        Creates a Command instance based on executor type and state
        that is specific to each type of command.
        :param service_state:
        :return:
        """
        if isinstance(self.executor, ExecutorAnsible):
            state = service_state.ansible_state
            restart = 'no'
            if service_state == self.ServiceDockerState.RESTARTED:
                restart = 'yes'

            print('name=%s state=%s restart=%s docker_host=%s'
                  % (self.name, state, restart, self.docker_host))

            docker_host_opt = 'docker_host=%s' % self.docker_host if self.docker_host else ''
            return CommandAnsible('name=%s state=%s restart=%s %s'
                                  % (self.name, state, restart, docker_host_opt),
                                  ansible_module='docker_container',
                                  stdout=True,
                                  timeout=self.TIMEOUT)
        elif isinstance(self.executor, ExecutorContainer):
            state = service_state.system_state
            return CommandContainer([], docker_command=state, stdout=True, timeout=self.TIMEOUT)
        else:
            return Command([])
