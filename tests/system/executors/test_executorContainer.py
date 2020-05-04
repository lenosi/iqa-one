import pytest

from iqa.system.executor.executor_container import ExecutorContainer
from iqa.system.executor.execution import Execution
from iqa.system.command.command_base import Command


class TestExecutorContainer:

    @pytest.fixture
    def executor(self, docker_services) -> ExecutorContainer:
        executor: ExecutorContainer = ExecutorContainer(
            name="Docker executor",
            container_name='sshd-container'
        )
        return executor

    def test_execute(self, executor: ExecutorContainer) -> None:

        cmd: Command = Command(args=["whoami"])

        execution: Execution = executor.execute(cmd)

        assert execution.completed_successfully()
