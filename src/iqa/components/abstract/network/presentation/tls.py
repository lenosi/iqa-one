from iqa.components.abstract.network.protocol.protocol import Protocol
from iqa.components.abstract.network.transport.tcp import TCP


class TLS11(Protocol):
    name: str = 'TLS 1.1'
    transport = TCP()


class TLS12(Protocol):
    name: str = 'TLS 1.2'
    transport = TCP()


class TLS13(Protocol):
    name: str = 'TLS 1.3'
    transport = TCP()
