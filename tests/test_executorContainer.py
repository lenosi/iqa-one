from iqa.system.executor.executor_container import ExecutorContainer
from iqa.system.command.command_base import Command


class TestExecutorContainer:
    def test_execute(self):
        executor = ExecutorContainer(
            name="Container executor",
            container_name='iqa-example-node'
        )

        cmd = Command(args=["whoami"])

        execution = executor.execute(cmd)

        assert execution.completed_successfully()
