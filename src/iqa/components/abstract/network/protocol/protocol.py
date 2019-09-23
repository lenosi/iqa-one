class Protocol:
    """ Protocol abstraction"""

    default_port = None

    def __init__(self, transport):
        self.name = type(self).__name__
        self.transport = transport
