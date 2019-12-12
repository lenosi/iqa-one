from iqa.components.abstract.network.protocol.protocol import Protocol


class TLS13(Protocol):
    def __init__(self) -> None:
        super(TLS13, self).__init__(self, transport)
        self.name: str = 'TLS 1.3'
