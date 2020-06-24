from iqa.system.command import CommandBase
from iqa.system.executor import ExecutionBase
from iqa.system.executor.localhost.executor import ExecutionAsyncio


class ExecutionDocker(ExecutionAsyncio):
    async def _run(self) -> None:
        pass

    def _docker_command(self, docker_host, docker_args, command):
        # define environment when docker_host provided
        env = dict()
        if docker_host:
            env['DOCKER_HOST'] = docker_host

        command_builder = CommandBase(args=docker_args, stdout=command.stdout, stderr=command.stderr,
                                      timeout=command.timeout, encoding=command.encoding)

        execution = ExecutionAsyncio(command=command_builder, env=env)
        return execution

    async def wait(self) -> None:
        pass

    def is_running(self) -> bool:
        pass

    def completed_successfully(self) -> bool:
        pass

    def on_timeout(self) -> None:
        pass

    def terminate(self) -> None:
        pass
