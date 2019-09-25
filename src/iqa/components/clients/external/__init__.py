import logging

from .client_external import ClientExternal
from .command.client_command import ClientCommand
from .java import *
from .nodejs import *
from .python import *


class ClientFactory(object):
    # Static element to store all available implementations
    _implementations: list = []

    @staticmethod
    def create_clients(implementation: str, node: Node, executor: Executor, **kwargs) -> list:

        for cl in ClientExternal.__subclasses__():

            # Ignore clients with different implementation
            if cl.implementation != implementation:
                continue

            # Now loop through concrete client types (sender, receiver, connector)
            clients = []
            for client_impl in cl.__subclasses__():
                name = '%s-%s-%s' % (implementation, client_impl.__name__.lower(), node.hostname)
                clients.append(client_impl(name=name, node=node, executor=executor, **kwargs))

            return clients

        exception = ValueError('Invalid client implementation: %s' % implementation)
        logging.getLogger(ClientFactory.__module__).error(exception)
        raise exception

    @staticmethod
    def get_available_implementations() -> list:

        # If implementations list has already been loaded, use it
        if ClientFactory._implementations:
            return ClientFactory._implementations

        result = []

        for cl in ClientExternal.__subclasses__():
            result.append(cl.implementation)

        ClientFactory._implementations = result

        return result
