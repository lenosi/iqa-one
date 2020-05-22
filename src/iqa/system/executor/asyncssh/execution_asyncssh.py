from typing import Optional, Union
from iqa.system.executor.execution import ExecutionBase


class ExecutionAsyncSsh(ExecutionBase):
    def _run(self) -> None:
        pass

    def wait(self) -> None:
        pass

    def is_running(self) -> bool:
        pass

    def completed_successfully(self) -> bool:
        pass

    def on_timeout(self) -> None:
        pass

    def terminate(self) -> None:
        pass

    def read_stdout(self, lines: bool = False) -> Optional[Union[str, list]]:
        pass

    def read_stderr(self, lines: bool = False) -> Optional[Union[str, list]]:
        pass
