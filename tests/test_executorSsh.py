from subprocess import run, PIPE

from iqa.system.executor.executor_ssh import ExecutorSsh
from iqa.system.command.command_base import Command


class TestExecutorSsh:
    def test_execute(self):
        ip_process = run(['docker', 'inspect', '-f', '"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"',
                                    'sshd-iqa'], stdout=PIPE)
        ip = ip_process.stdout.decode('utf-8').strip('\n\"')

        executor = ExecutorSsh(
            user="root",
            hostname=ip,
            name="SSH executor",
            ssl_private_key="tests/images/sshd_image/identity"
        )

        cmd = Command(args=["whoami"])

        execution = executor.execute(cmd)

        assert execution.completed_successfully()
