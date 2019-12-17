from iqa.abstract.server.broker import Broker
from iqa.system.executor import Executor
from iqa.system.node.node import Node
from iqa.system.service.service import Service


class BrokerFactory(object):

    @staticmethod
    def create_broker(implementation: str, node: Node, executor: Executor, service_impl: Service, **kwargs):

        for broker in Broker.__subclasses__():

            # Ignore broker with different implementation
            if broker.implementation != implementation:
                continue

            name: str = '%s-%s-%s' % ('broker', broker.__name__, node.hostname)
            return broker(name=name, node=node, executor=executor, service=service_impl, **kwargs)  # type: ignore

        raise ValueError('Invalid broker implementation: %s' % implementation)
