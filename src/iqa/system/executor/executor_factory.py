from iqa.system.executor import Executor, ExecutorLocal, ExecutorSsh, ExecutorContainer, ExecutorAnsible
from iqa.system.executor.executor_kubernetes import ExecutorKubernetes


class ExecutorFactory(object):
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
