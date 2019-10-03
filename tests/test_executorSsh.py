import subprocess
import logging

from iqa.system.executor.executor_ssh import ExecutorSsh
from iqa.system.command.command_base import Command
from iqa.system.executor.executor_local import ExecutorLocal

logging.basicConfig(level=logging.DEBUG)


class TestExecutorSsh:
    def test_execute(self):
        cmd_ip = Command(['docker', 'inspect', '-f', '"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"',
                          'sshd-iqa'], stdout=True)
        local_exec = ExecutorLocal()
        ip_ex = local_exec.execute(command=cmd_ip)
        ip_ex.wait()
        ip = ip_ex.read_stdout().decode('utf-8').rstrip().lstrip()
        executor = ExecutorSsh(
            user="root",
            hostname=ip,
            name="SSH executor",
            ssl_private_key="tests/images/sshd_image/identity",
        )

        cmd = Command(args=["whoami"], stdout=True)

        execution = executor.execute(cmd,)
        execution.wait()
        assert execution.completed_successfully()
        assert execution.read_stdout().rstrip().lstrip() == "root"
