from iqa.components.abstract.network.protocol import Protocol


class AMQP10(Protocol):
    """
    AMQP 1.0 Protocol implementation
    """
    default_port = 5672

    def __init__(self, transaction, transport):
        super().__init__(transaction, transport)
