from iqa.components.abstract.network.protocol import Protocol
from iqa.components.abstract.network.transport import TCP


class Stomp(Protocol):
    def __init__(self, transport=TCP) -> None:
        super(Stomp, self).__init__(transport)
