from iqa.components.abstract.network.protocol.protocol import Protocol


class AMQP10(Protocol):
    """
    AMQP 1.0 Protocol implementation
    """
    default_port: int = 5672

    def __init__(self, transport) -> None:
        super().__init__(transport)
