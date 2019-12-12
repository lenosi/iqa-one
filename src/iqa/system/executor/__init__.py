from .executor_ansible import ExecutorAnsible
from .executor_base import Executor
from .executor_container import ExecutorContainer
from .executor_kubernetes import ExecutorKubernetes
from .executor_local import ExecutorLocal
from .executor_ssh import ExecutorSsh

from iqa.utils.types import ExecutorType


class ExecutorFactory(object):
    """
    Loops through all implementations of the Executor class
    and returns an instance of the executor initialized from kwargs.
    """

    @staticmethod
    def create_executor(exec_impl: str = 'ansible', **kwargs) -> ExecutorType:

        for exec_class in Executor.__subclasses__():
            if exec_class.implementation != exec_impl:
                continue

            return exec_class(**kwargs)

        raise ValueError('Invalid Executor implementation given: %s' % exec_impl)


class ExecutorFactory2(object):
    @staticmethod
    def create_executor(impl: str, **kwargs) -> Executor:
        if impl == ExecutorLocal.implementation:
            return ExecutorLocal()
        elif impl == ExecutorSsh.implementation:
            return ExecutorSsh(**kwargs)
        elif impl == ExecutorContainer.implementation:
            return ExecutorContainer(**kwargs)
        elif impl == ExecutorAnsible.implementation:
            return ExecutorAnsible(**kwargs)
        elif impl == ExecutorKubernetes.implementation:
            return ExecutorKubernetes(**kwargs)
        else:
            raise ValueError('Invalid executor implementation')
