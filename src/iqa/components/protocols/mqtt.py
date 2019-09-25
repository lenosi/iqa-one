from iqa.components.abstract.network.protocol import Protocol
from iqa.components.abstract.network.transport import TCP


class Mqtt(Protocol):
    def __init__(self, transport=TCP):
        super(Mqtt, self).__init__(transport)
