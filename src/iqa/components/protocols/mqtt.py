from iqa.components.abstract.network.protocol.protocol import Protocol
from iqa.components.abstract.network.transport.tcp import TCP


class MQTT(Protocol):
    name: str = 'MQTT'
    default_port = 1883
    transport = TCP()


class MQTToverTLS(Protocol):
    name: str = 'MQTT'
    default_port = 8883
    transport = TCP()
