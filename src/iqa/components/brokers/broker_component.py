from iqa.abstract import Broker
from iqa.components.abstract.server import ServerComponent


class BrokerComponent(Broker, ServerComponent):
    def __init__(self, name: str, **kwargs) -> None:
        super(BrokerComponent, self).__init__(name, **kwargs)
