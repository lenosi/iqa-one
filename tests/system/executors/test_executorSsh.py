from subprocess import check_output

from iqa.system.executor.execution import Execution
from iqa.system.executor.executor_ssh import ExecutorSsh
from iqa.system.command.command_base import Command


class TestExecutorSsh:
    def test_execute(self) -> None:
        ip: str = check_output(
            ['docker', 'inspect', '-f', '"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"',
             'sshd-iqa'], encoding='utf-8').strip('\n\"')

        executor: ExecutorSsh = ExecutorSsh(
            user="root",
            hostname=ip,
            name="SSH executor",
            ssl_private_key="tests/images/sshd_image/identity"
        )

        cmd: Command = Command(args=["whoami"])

        execution: Execution = executor.execute(cmd)

        assert execution.completed_successfully()
