"""
Interface for Node element. A node holds a running messaging component and it
must provide some basic behaviors, like ping, get_ip and execute command.
"""
import abc
from typing import Optional, TYPE_CHECKING

from iqa.system.command.command_base import Command
from iqa.system.executor.execution import Execution
if TYPE_CHECKING:
    from iqa.utils.types import ExecutorType


class Node:
    """Node abstract component"""

    def __init__(self, hostname: str, executor: 'ExecutorType', name: str = None,
                 ip: str = None) -> None:
        self.hostname: str = hostname
        self.name: str = name if name else hostname
        self.executor: ExecutorType = executor
        self.ip: Optional[str] = ip

    def execute(self, command: Command) -> Execution:
        """Execute command using Node's executor"""
        return self.executor.execute(command)

    @abc.abstractmethod
    def ping(self) -> bool:
        pass

    @abc.abstractmethod
    def get_ip(self) -> Optional[str]:
        pass
