from iqa.system.command.command_base import CommandBase


class CommandBaseAnsible(CommandBase):
    """
    Simple extension of the Command class that can be used along with the
    ExecutorAnsible in which this command can also provide the ansible
    module to use. When doing so, the 'ansible_args' parameter will be a
    single string containing exactly the same args syntax used in the CLI,
    when calling the respective module. Example: 'filter=ansible_hostname'.
    """

    def __init__(
        self,
        ansible_args: str = '',
        ansible_module: str = 'raw',
        stdout: bool = False,
        stderr: bool = False,
        daemon: bool = False,
        timeout: int = 0,
        encoding: str = 'utf-8',
    ) -> None:
        super(CommandBaseAnsible, self).__init__(
            [ansible_args], stdout, stderr, daemon, timeout, encoding
        )
        self.ansible_module: str = ansible_module
