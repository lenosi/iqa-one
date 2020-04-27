from iqa.components.abstract.network.protocol.protocol import Protocol
from iqa.components.abstract.network.transport.tcp import TCP
from iqa.utils.singleton import Singleton


class _AMQP(Protocol):
    name: str = 'AMQP Advanced Message Queuing Protocol'
    default_port: int = 5672
    transport = TCP()


@Singleton
class AMQP10(_AMQP):
    name: str = 'AMQP Advanced Message Queuing Protocol 1.0'


@Singleton
class AMQP091(_AMQP):
    name: str = 'AMQP Advanced Message Queuing Protocol 0.9.1'
