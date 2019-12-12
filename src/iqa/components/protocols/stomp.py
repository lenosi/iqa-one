from iqa.components.abstract.network.protocol.protocol import Protocol
from iqa.components.abstract.network.transport.tcp import TCP


class Stomp(Protocol):
    def __init__(self, transport=TCP) -> None:
        super(Stomp, self).__init__(transport)
