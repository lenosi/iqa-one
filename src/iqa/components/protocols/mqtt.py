from iqa.components.abstract.network.protocol import Protocol
from iqa.components.abstract.network.transport import TCP


class Mqtt(Protocol):
    def __init__(self, transport=TCP, default_port=5672):
        super(Mqtt, self).__init__(transport, default_port)
