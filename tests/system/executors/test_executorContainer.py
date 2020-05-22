import pytest

from iqa.system.executor.docker.executor_docker import ExecutorDocker
from iqa.system.executor import ExecutionBase
from iqa.system.command.command_base import CommandBase


class TestExecutorContainer:

    @pytest.fixture
    def executor(self, docker_services) -> ExecutorDocker:
        executor: ExecutorDocker = ExecutorDocker(
            name="Docker executor",
            container_name='sshd-container'
        )
        return executor

    def test_execute(self, executor: ExecutorDocker) -> None:

        cmd: CommandBase = CommandBase(args=["whoami"])

        execution: ExecutionBase = executor.execute(cmd)

        assert execution.completed_successfully()
