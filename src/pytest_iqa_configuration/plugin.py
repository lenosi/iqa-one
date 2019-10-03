"""PyTest Ansible Plugin
Defines mandatory options and configuration that can be applied to all test suites.
"""

import atexit
import os

from .logger import get_logger

# Default timeout settings
DEFAULT_LOG_FORMAT = '%(asctime)s [%(levelname)s] (%(pathname)s:%(lineno)s) - %(message)s'
DEFAULT_LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
cleanup_file_list = []

# linting
# (iqa)

log = get_logger(__name__)


def pytest_addoption(parser):
    """Add options to control ansible."""


    # Default values for pytest.ini files (if absent)
    parser.addini('log_level',
                  default='WARNING',
                  type=None,
                  help='logging level used by the logging module')

    parser.addini('log_format',
                  default=DEFAULT_LOG_FORMAT,
                  type=None,
                  help='log format as used by the logging module.')

    parser.addini('log_date_format',
                  default=DEFAULT_LOG_DATE_FORMAT,
                  type=None,
                  help='log date format as used by the logging module.')

    parser.addini('log_cli',
                  default=True,
                  type='bool',
                  help='enable log display during test run (also known as "live logging").')


def cleanup_files():
    """
    Remove temporary files.
    :return:
    """
    for f in cleanup_file_list:
        os.unlink(f)


def pytest_configure(config):
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
        if type(value) != list:
            continue
        for n in range(len(value)):
            new_options.update({'%s_%d' % (key, n): str(value[n])})

    options.update(new_options)
    options = {key: str(value) for (key, value) in options.items() if key not in os.environ}
    os.environ.update(options)

    # Loading the inventory
    iqa = Instance(inventory=config.getvalue('inventory'), cli_args=config.option.__dict__)

    # Adjusting clients timeout
    for client in iqa.clients:
        client.command.control.timeout = CLIENTS_TIMEOUT

    config.iqa = iqa

    # Clean up temporary files at exit
    atexit.register(cleanup_files)


def pytest_runtest_call(item):
    """
    Hook that runs before each test method and can iterate through
    parametrized items adding a generic "param:<argname>":"<argvalue>"
    to the user_properties dictionary.

    When generating a junit xml, these params will be added as "<property>"
    elements for each test case.

    If test method takes no parameter, then nothing will be added.
    :param item:
    :return:
    """

    if not hasattr(item, 'callspec'):
        return

    for (argname, argvalue) in item.callspec.params.items():
        item.user_properties.append(('param:%s' % argname, argvalue))
