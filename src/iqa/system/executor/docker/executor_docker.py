from typing import Optional

from iqa.system.executor.executor import ExecutorBase
from iqa.system.command.command_base import CommandBase
from iqa.system.executor.asyncio_localhost.execution import ExecutionAsyncio
from iqa.system.command.command_container import CommandBaseContainer

"""
Executor instance that runs a given Command instance using
Docker CLI against a pre-defined container (by name or id).
"""


class ExecutorDocker(ExecutorBase):
    """
    Executor that runs Command instances in a Docker container.
    """

    implementation: str = 'docker'

    def __init__(
        self,
        name: str = 'ExecutorDocker',
        container_name: str = '',
        user: str = ''
    ):
        super(ExecutorDocker, self).__init__()
        self.container_name: str = container_name
        self.name: str = name
        self.user: str = user
        self.docker_host: str = ''
        self._command: Optional[CommandBaseContainer] = None

    async def _execute(self, command: CommandBase = None, user: str = '') -> ExecutionAsyncio:

        docker_args: list = ['docker']

        if isinstance(command, CommandBaseContainer):
            # Logging docker command to use
            self._logger.debug('Using docker command: {}'.format(command.docker_command))
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

        execution = ExecutionAsyncio(command=command, modified_args=docker_args, env=env)
        await execution.run()
        return execution
