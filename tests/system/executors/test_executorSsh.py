import logging
import sys

import asyncssh
import pytest

from iqa.system.executor.asyncssh import ConnectionAsyncSsh
from iqa.system.node import NodeDocker

from iqa.utils.tcp_util import wait_host_port


class TestExecutorSsh:
    @pytest.mark.asyncio
    async def test_asyncssh_connection(self, node: NodeDocker):
        await wait_host_port(node.ip, port=22)

        try:
            c = ConnectionAsyncSsh(
                host=node.ip,
                port=22,
                username='root',
                password='SomeSecretPassword0987',
                known_hosts=None,
                client_keys=None
            )
            await c.connect()
            await c.disconnect()
        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))

    @pytest.mark.asyncio
    async def test_command(self, node: NodeDocker):
        await wait_host_port(node.ip, port=22)
        con = ConnectionAsyncSsh(
            host=node.ip,
            port=22,
            username='root',
            password='SomeSecretPassword0987',
            known_hosts=None,
            client_keys=None
        )
        await con.connect()
        result = await con.run('echo "Hello World!"')
        await con.disconnect()
        print(result.stdout, end='')

    @pytest.mark.asyncio
    async def test_session(self, node: NodeDocker):
        await wait_host_port(node.ip, port=22)
        con = ConnectionAsyncSsh(
            host=node.ip,
            port=22,
            username='root',
            password='SomeSecretPassword0987',
            known_hosts=None,
            client_keys=None
        )
        await con.connect()
        session = await con.new_session()
        await con.disconnect()
