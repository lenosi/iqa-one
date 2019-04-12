from .transport import Transport


class WebSocket(Transport):
    def __init__(self):
        Transport.__init__(self)
        self.name = None
        pass
