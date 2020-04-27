from iqa.utils.singleton import Singleton
from .transport import Transport


@Singleton
class WebSocket(Transport):
    name:str = 'WebSocket'
