from iqa.components.abstract.network.protocol.protocol import Protocol
from iqa.components.abstract.network.transport.tcp import TCP


class STOMP(Protocol):
    name: str = 'STOMP'
    default_port = 1883
    transport = TCP()
