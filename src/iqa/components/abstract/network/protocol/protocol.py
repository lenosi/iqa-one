class Protocol:
    """ Protocol abstraction"""

    default_port = None

    def __init__(self, transaction, transport):
        self.name = type(self).__name__
        self.transaction = transaction
        self.transport = transport
