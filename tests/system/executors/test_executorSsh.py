from subprocess import check_output
import subprocess
import logging

from iqa.system.executor.execution import Execution
from iqa.system.executor.executor_local import ExecutorLocal
from iqa.system.executor.executor_ssh import ExecutorSsh
from iqa.system.command.command_base import Command

logging.basicConfig(level=logging.DEBUG)


class TestExecutorSsh:
    def test_execute(self) -> None:
        cmd_ip = Command(
            ['docker', 'inspect', '-f', '"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"',
             'sshd-iqa'], stdout=True)
        local_exec = ExecutorLocal()
        ip_ex = local_exec.execute(command=cmd_ip)
        ip_ex.wait()
        ip = ip_ex.read_stdout().decode('utf-8').rstrip().lstrip()

        executor: ExecutorSsh = ExecutorSsh(
            user="root",
            hostname=ip,
            name="SSH executor",
            ssl_private_key="tests/images/sshd_image/identity"
        )

        cmd: Command = Command(args=["whoami"], stdout=True)

        execution: Execution = executor.execute(cmd)
        execution.wait()
        assert execution.completed_successfully()
        assert execution.read_stdout().rstrip().lstrip() == "root"