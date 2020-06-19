import logging
from enum import Enum
from typing import Optional

from docker.errors import APIError, NotFound

from iqa.system.command.command_ansible import CommandBaseAnsible
from iqa.system.command.command_base import CommandBase
from iqa.system.executor.ansible.executor_ansible import ExecutorAnsible
from iqa.system.executor.docker.executor_docker import ExecutorDocker
from iqa.system.executor import ExecutionBase
from iqa.system.service.service import Service, ServiceStatus
from iqa.utils.docker_util import get_container


class ServiceDocker(Service):
    """
    Implementation of a service represented by a docker container.
    So startup and shutdown are done by managing current state of related
    docker container name.
    """

    _logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, name: str, executor: ExecutorDocker) -> None:
        super().__init__(name, executor)
        self.docker_host: Optional[str] = executor.docker_host

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
            container = get_container(name=self.name)
            if not container:
                ServiceDocker._logger.debug('Service: %s - Status: UNKNOWN' % self.name)
                return ServiceStatus.UNKNOWN

            if container.status == 'running':
                ServiceDocker._logger.debug('Service: %s - Status: RUNNING' % self.name)
                return ServiceStatus.RUNNING
            elif container.status == 'exited':
                ServiceDocker._logger.debug('Service: %s - Status: STOPPED' % self.name)
                return ServiceStatus.STOPPED
        except APIError or NotFound:
            ServiceDocker._logger.exception(
                'Error retrieving status of docker container'
            )
            return ServiceStatus.FAILED

        return ServiceStatus.UNKNOWN

    async def start(self) -> ExecutionBase:
        return await self.executor.execute(
            self._create_command(self.ServiceDockerState.STARTED)
        )

    async def stop(self) -> ExecutionBase:
        return await self.executor.execute(
            self._create_command(self.ServiceDockerState.STOPPED)
        )

    async def restart(self) -> ExecutionBase:
        return await self.executor.execute(
            self._create_command(self.ServiceDockerState.RESTARTED)
        )

    def enable(self) -> Optional[ExecutionBase]:
        """
        Simply ignore it (not applicable to containers)
        :return:
        """
        return None

    def disable(self) -> Optional[ExecutionBase]:
        """
        Simply ignore it (not applicable to containers)
        :return:
        """
        return None

    def _create_command(self, service_state: ServiceDockerState) -> CommandBase:
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

            print(
                'name=%s state=%s restart=%s docker_host=%s'
                % (self.name, state, restart, self.docker_host)
            )

            docker_host_opt = (
                'docker_host=%s' % self.docker_host if self.docker_host else ""
            )
            return CommandBaseAnsible(
                'name=%s state=%s restart=%s %s'
                % (self.name, state, restart, docker_host_opt),
                ansible_module='docker_container',
                stdout=True,
                timeout=self.TIMEOUT,
            )
        elif isinstance(self.executor, ExecutorDocker):
            state = service_state.system_state
            return CommandBase(['docker', state, self.executor.container_name])
        else:
            return CommandBase([])
