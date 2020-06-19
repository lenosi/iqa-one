import pytest

from iqa.system.executor.localhost.executor import ExecutorAsyncio
from iqa.system.executor.localhost.execution import ExecutionAsyncio

from iqa.system.command.command_base import CommandBase


class TestExecutorContainer:

    @pytest.fixture
    def executor(self) -> ExecutorAsyncio:
        executor: ExecutorAsyncio = ExecutorAsyncio(
            name="Localhost executor"
        )
        return executor

    # @pytest.mark.asyncio
    # async def test_execute(self, executor: ExecutorAsyncio) -> None:
    #
    #     cmd: CommandBase = CommandBase(args=["whoami"])
    #
    #     execution: ExecutorAsyncio = executor.execute(cmd)
    #     await execution.wait()
    #
    #     assert execution.completed_successfully()

    @pytest.mark.asyncio
    async def test_execution(self) -> None:
        cmd: CommandBase = CommandBase(args=["whoami"])

        execution: ExecutionAsyncio = ExecutionAsyncio(command=cmd)

        await execution.run()
        await execution.wait()

        assert execution.completed_successfully()
