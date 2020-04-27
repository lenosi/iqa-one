from iqa.components.abstract.network.transport.transport import Transport
from iqa.utils.singleton import Singleton


@Singleton
class TCP(Transport):
    name: str = 'TCP Transport Protocol'
