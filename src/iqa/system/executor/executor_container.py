from typing import Optional

from .execution import ExecutionProcess
from .executor_base import Executor
from ..command.command_base import Command
from ..command.command_container import CommandContainer

"""
Executor instance that runs a given Command instance using
Docker CLI against a pre-defined container (by name or id).
"""


class ExecutorContainer(Executor):
    """
    Executor that runs Command instances in a Docker container.
    """

    implementation: str = 'docker'

    def __init__(
        self,
        name: str = 'ExecutorContainer',
        container_name: str = '',
        user: str = ''
    ):
        super(ExecutorContainer, self).__init__()
        self.container_name: str = container_name
        self.name: str = name
        self.user: str = user
        self.docker_host: str = ''

    def _execute(self, command: Command, user: str = '') -> ExecutionProcess:

        docker_args: list = ['docker']

        if isinstance(command, CommandContainer):
            # Logging docker command to use
            self._logger.debug('Using docker command: %s' % command.docker_command)
            docker_args.append(command.docker_command)
        else:
            docker_args.append('exec')

        if user:
            docker_args += ['-u', user]
        elif self.user:
            docker_args += ['-u', self.user]

        docker_args.append(self.container_name)
        docker_args += command.args

        # define environment when docker_host provided
        env = dict()
        if self.docker_host:
            env['DOCKER_HOST'] = self.docker_host

        # Set new args
        return ExecutionProcess(command, self, modified_args=docker_args, env=env)
