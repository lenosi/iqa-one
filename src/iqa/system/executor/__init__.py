import logging
from typing import Any

from iqa.system.executor.ansible import *
from iqa.system.executor.asyncssh import *
from iqa.system.executor.docker import *
from iqa.system.executor.kubernetes import *
from iqa.system.executor.localhost import *
from iqa.system.executor.ssh import *
from iqa.system.executor.execution import ExecutionBase
from iqa.system.executor.executor import ExecutorBase
from iqa.utils.types import ExecutorType
from iqa.utils.utils import get_subclasses

logger = logging.getLogger(__name__)


def create_executor(implementation: str, **kwargs) -> ExecutorType:
    """
        Loops through all implementations of the Executor class
        and returns an instance of the executor initialized from kwargs.

    Args:
        implementation:
        **kwargs:

    Returns:

    """
    try:
        ex: Any = get_subclasses(
            given_name=implementation,
            in_class=ExecutorBase,
            in_class_property='implementation'
        )
        return ex(**kwargs)  # type: ExecutorType
    except ValueError:
        logger.error('Implementation of "%s" executor was not found!' % implementation)
