from iqa.abstract.listener import Listener
from iqa.abstract.server.messaging_server import MessagingServer


class Router(MessagingServer):
    """
    Abstract abstract Router
    """

    def get_url(self, port: int = None, listener: Listener = None) -> str:
        return NotImplemented

    def __init__(self, **kwargs) -> None:
        super(Router, self).__init__()
