from iqa.components.abstract.network.protocol import Protocol
from iqa.components.abstract.network.transport import TCP


class Amqp(Protocol):
    default_port = 5672
    def __init__(self, transport=TCP):
        super(Amqp, self).__init__(transport)
        self.name = "AMQP"


class Amqp10(Amqp):
    def __init__(self, transport=TCP):
        super(Amqp10, self).__init__(transport)
        self.name = "AMQP 1.0"


class Amqp091(Amqp):
    def __init__(self, transport=TCP):
        super(Amqp091, self).__init__(transport)
        self.name = "AMQP 0.9.1"
