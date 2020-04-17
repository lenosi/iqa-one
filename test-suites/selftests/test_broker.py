from iqa.utils.types import BrokerType
from iqa.system.node.node import Node


def test_isinstance(broker: BrokerType):
    assert isinstance(broker, BrokerType)


def test_node(broker: BrokerType):
    assert isinstance(broker.node, Node)


def test_node_ip(broker: BrokerType):
    print(broker.node.ip)
    assert broker.node.ip


def test_exec_on_broker_node(broker: BrokerType):
    execution = broker.node.execute(['ls'])
    assert True if execution.get_ecode() == 0 else False
