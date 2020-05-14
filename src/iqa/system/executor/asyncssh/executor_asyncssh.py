import os
import asyncio
import asyncssh

from iqa.system.executor.executor import Executor
from iqa.system.executor.execution import Execution
from iqa.system.command.command_base import Command

"""
Runs a command using SSH CLI.
"""


class ExecutorSsh(Executor):
    """
    Executor that runs Command instances via SSH
    """
    implementation = 'ssh'

    def __init__(self, name, ip, port=22, private_key=None, password=None, user='root', **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.ip = ip
        self.port = port
        self.private_key = private_key
        self.user = user
        self.password = password
        self.session = self.new_session()

    def _execute(self, command: Command) -> Execution:
        pass

    async def new_session(self):
        session = await asyncssh.connect(
            host=self.ip,
            username=self.user,
            password=self.password,
            known_hosts=None,
            client_keys=None
            # client_keys=[key]
        )
        return session


