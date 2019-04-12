from iqa.messaging.abstract.server.messaging_server import MessagingServer


class Router(MessagingServer):
    """
    Abstract abstract Router
    """

    def __init__(self, name: str, **kwargs):
        super(Router, self).__init__()
