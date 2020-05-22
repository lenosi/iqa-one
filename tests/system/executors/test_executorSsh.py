import nest_asyncio

import logging
import sys

import asyncssh
import pytest

from iqa.system.executor.asyncssh import ExecutorAsyncSsh, ExecutionAsyncSsh
from iqa.system.node import NodeDocker

from asyncio.events import AbstractEventLoop

from iqa.utils.tcp_util import wait_host_port


async def run_client(ip):
    await wait_host_port(ip, port=22)
    async with asyncssh.connect(
            ip,
            username='root',
            password='SomeSecretPassword0987',
            known_hosts=None,
            client_keys=None
            # client_keys=[key]
            ) as conn:
        result = await conn.run('ls', check=True)
        print(result.stdout, end='')


class TestExecutorSsh:

    # @pytest.fixture
    # def executor(self, node: NodeDocker) -> ExecutorSshOld:
    #     executor: ExecutorSshOld = ExecutorSshOld(
    #         name="Docker executor",
    #         hostname=node.host,
    #         ssl_private_key="../../devel/images/centos8-init-sshd/identity"
    #     )
    #     return executor
    #
    # @pytest.fixture
    # async def executor(self, node: NodeDocker) -> ExecutorAsyncSsh:
    #     executor: ExecutorAsyncSsh = ExecutorAsyncSsh(
    #         name="Docker executor",
    #         user='root',
    #         host=node.ip,
    #         password='SomeSecretPassword0987',
    #         known_hosts=None,
    #         client_keys=None
    #     )
    #     return executor

    @pytest.mark.asyncio
    async def test_evloop(self, event_loop: AbstractEventLoop, node: NodeDocker):
        # await asyncio.sleep(0, loop=event_loop)

        nest_asyncio.apply()
        try:
            event_loop.run_until_complete(run_client(ip=node.ip))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))
        logging.basicConfig(level=logging.DEBUG)

    @pytest.mark.asyncio
    async def test_asyncssh_session(self, event_loop: AbstractEventLoop, node: NodeDocker):
        # session = await executor.new_session()

        async def task():
            executor: ExecutorAsyncSsh = ExecutorAsyncSsh(
                name="Docker executor",
                user='root',
                host=node.ip,
                password='SomeSecretPassword0987',
                known_hosts=None,
                client_keys=None
            )
            session = await executor._send_command('ls')
            logging.debug(session)

        event_loop.run_until_complete(task())
        assert True
    #
    # def test_execute(self, executor: ExecutorSshOld, event_loop: AbstractEventLoop) -> None:
    #     cmd: Command = Command(args=["whoami"], stdout=True)
    #
    #     execution: Execution = executor.execute(cmd)
    #     execution.wait()
    #     assert execution.completed_successfully()
    #     assert execution.read_stdout().rstrip().lstrip() == "root"
