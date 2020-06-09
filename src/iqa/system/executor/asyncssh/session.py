import sys
from typing import Optional

from asyncssh import SSHClientSession, EXTENDED_DATA_STDERR, SSHWriter, SSHReader

MAX_BUFFER = 65535


class AsyncSSHClientSession(SSHClientSession):
    def connection_lost(self, exc):
        if exc:
            print('SSH session error: ' + str(exc), file=sys.stderr)


class AsyncSSHSession:
    def __init__(self):
        self._stdin: Optional[SSHWriter] = None
        self._stdout: Optional[SSHReader] = None
        self._stderr: Optional[SSHReader] = None

    async def send(self, cmd: str) -> None:
        """ Send command """
        self._stdin.write(cmd)

    async def read(self) -> str:
        """ Read buffer """
        output = await self._stdout.read(MAX_BUFFER)
        return output
