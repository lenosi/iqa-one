from iqa.components.abstract.network.protocol import Protocol
from iqa.components.abstract.network.transport import TCP


class Openwire(Protocol):
    def __init__(self, transport=TCP) -> None:
        super(Openwire, self).__init__(transport)
