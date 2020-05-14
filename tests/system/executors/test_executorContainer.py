import pytest

from iqa.system.executor.docker.executor_docker import ExecutorDocker
from iqa.system.executor import Execution
from iqa.system.command.command_base import Command


class TestExecutorContainer:

    @pytest.fixture
    def executor(self, docker_services) -> ExecutorDocker:
        executor: ExecutorDocker = ExecutorDocker(
            name="Docker executor",
            container_name='sshd-container'
        )
        return executor

    def test_execute(self, executor: ExecutorDocker) -> None:

        cmd: Command = Command(args=["whoami"])

        execution: Execution = executor.execute(cmd)

        assert execution.completed_successfully()
