from iqa.components.abstract.network.protocol.protocol import Protocol


class TLS12(Protocol):
    def __init__(self) -> None:
        super(TLS12, self).__init__(self, transport)
        self.name: str = 'TLS 1.2'
