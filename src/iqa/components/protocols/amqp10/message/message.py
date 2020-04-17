import iqa
from iqa.abstract.message.message import Message as AbstractMessage


class Message(AbstractMessage):
    """
    AMQP10 Message
    """

    def __init__(self) -> None:
        iqa.abstract.message.message.Message.__init__(self)
