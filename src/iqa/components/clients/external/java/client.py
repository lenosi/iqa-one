from iqa.components import protocols
from iqa.components.abstract.component import Component
from iqa.components.clients.external import ClientExternal


class ClientJava(ClientExternal, Component):
    """Java Qpid JMS client (base abstract class)."""

    supported_protocols = [protocols.Amqp10()]
    implementation = 'java'
    version = '1.0.1'

    def __init__(self, name: str, node, **kwargs):
        super(ClientJava, self).__init__(name, node, **kwargs)
