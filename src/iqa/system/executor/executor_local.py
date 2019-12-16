from .execution import Execution
from .executor_base import Executor

"""
Runs a local command using SSH CLI.
"""


class ExecutorLocal(Executor):
    """
    Executes a given command locally.
    """

    implementation = "local"

    def __init__(self, name: str = "ExecutorLocal", **kwargs) -> None:
        super(ExecutorLocal, self).__init__(**kwargs)
        self.name: str = name

    def _execute(self, command) -> Execution:
        return Execution(command, self)  # type: ignore
