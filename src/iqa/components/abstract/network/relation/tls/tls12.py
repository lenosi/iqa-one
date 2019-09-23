from iqa.components.abstract.network.protocol import Protocol


class TLS12(Protocol):
    def __init__(self):
        Protocol.__init__(self)
        self.name = 'TLS 1.2'
