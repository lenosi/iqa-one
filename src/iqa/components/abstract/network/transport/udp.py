from iqa.components.abstract.network.transport.transport import Transport
from iqa.utils.singleton import Singleton


@Singleton
class UDP(Transport):
    name: str = 'UDP Transport Protocol'
