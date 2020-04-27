from iqa.components.abstract.network.protocol.protocol import Protocol
from iqa.components.abstract.network.transport.tcp import TCP


class Openwire(Protocol):
    default_port = 1883
    transport = TCP()
