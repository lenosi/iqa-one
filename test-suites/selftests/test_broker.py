from iqa.components.brokers import Broker
from iqa.system.node import Node


def test_isinstance(broker: Broker):
    assert isinstance(broker, Broker)


def test_node(broker: Broker):
    assert isinstance(broker.node, Node)


def test_node_ip(broker: Broker):
    print(broker.node.ip)
    assert broker.node.ip


def test_exec_on_broker_node(broker: Broker):
    exec = broker.node.execute(['ls'])
    assert True if exec.get_ecode() == 0 else False
