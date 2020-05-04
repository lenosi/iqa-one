import pytest
import logging

from iqa.system.executor.execution import Execution
from iqa.system.executor.executor_ssh import ExecutorSsh
from iqa.system.command.command_base import Command
from iqa.system.node import NodeDocker

logging.basicConfig(level=logging.DEBUG)


class TestExecutorSsh:

    @pytest.fixture
    def executor(self, docker_services, node: NodeDocker) -> ExecutorSsh:
        executor: ExecutorSsh = ExecutorSsh(
            name="Docker executor",
            hostname=node.ip,
            ssl_private_key="../../devel/images/centos8-init-sshd/identity"
        )
        return executor

    def test_execute(self, executor: ExecutorSsh) -> None:
        cmd: Command = Command(args=["whoami"], stdout=True)

        execution: Execution = executor.execute(cmd)
        execution.wait()
        assert execution.completed_successfully()
        assert execution.read_stdout().rstrip().lstrip() == "root"