from iqa.components.abstract.network.protocol.protocol import Protocol
from iqa.utils.singleton import Singleton


@Singleton
class AMQP10(Protocol):
    """
    AMQP 1.0 Protocol implementation
    """

    default_port: int = 5672
