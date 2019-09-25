import iqa
from iqa.abstract import Message as AbstractMessage


class Message(AbstractMessage):
    """
    AMQP10 Message
    """

    def __init__(self):
        iqa.iqa.abstract.message.Message.__init__(self)
