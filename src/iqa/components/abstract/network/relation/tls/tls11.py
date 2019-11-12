from iqa.components.abstract.network.protocol import Protocol


class TLS11(Protocol):
    def __init__(self) -> None:
        Protocol.__init__(self, transport)
        self.name: str = 'TLS 1.1'
