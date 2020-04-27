"""PyTest Ansible Plugin
Defines mandatory options and configuration that can be applied to all test suites.
"""

import atexit
import os

from iqa.instance.instance import Instance
from .logger import get_logger

# Default timeout settings
CLIENTS_TIMEOUT: int = 60
cleanup_file_list: list = []

# linting
# (iqa)

log = get_logger(__name__)


def pytest_addoption(parser) -> None:
    """Add options to control ansible."""

    group = parser.getgroup('pytest-iqa')
    group.addoption(
        '--inventory',
        action='store',
        dest='inventory',
        required=True,
        metavar='INVENTORY',
        help='Inventory file to use',
    )


def cleanup_files() -> None:
    """
    Remove temporary files.
    :return:
    """
    for f in cleanup_file_list:
        os.unlink(f)


def pytest_configure(config) -> None:
    """
    Loads IQAInstance based on provided environment and extra command line args.
    All arguments will be available as variables that can be used inside the inventory.
    The same can be done when using Ansible CLI (using -e cli_arg=value).
    :param config:
    :return:
    """

    # Adding all arguments as environment variables, so child executions of Ansible
    # will be able to use the same variables.
    options = dict(config.option.__dict__)

    # Insert array elements with _0, _1, such as --router 1.1.1.1 and --router 2.2.2.2
    # would become: router_0: 1.1.1.1 and router_1: 2.2.2.2
    new_options = dict()
    for (key, value) in options.items():
        if not isinstance(value, list):
            continue
        for n in range(len(value)):
            new_options.update({'%s_%d' % (key, n): str(value[n])})

    options.update(new_options)
    options = {
        key: str(value) for (key, value) in options.items() if key not in os.environ
    }
    os.environ.update(options)

    # Loading the inventory
    iqa = Instance(
        inventory=config.getvalue('inventory'), cli_args=config.option.__dict__
    )

    # Adjusting clients timeout
    for client in iqa.clients:
        client.command.control.timeout = CLIENTS_TIMEOUT

    config.iqa = iqa

    # Clean up temporary files at exit
    atexit.register(cleanup_files)
