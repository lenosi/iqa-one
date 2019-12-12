from iqa.components.abstract.network.protocol.protocol import Protocol
from iqa.components.abstract.network.transport.tcp import TCP


class Mqtt(Protocol):
    def __init__(self, transport=TCP) -> None:
        super(Mqtt, self).__init__(transport)
