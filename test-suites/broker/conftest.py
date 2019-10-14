import pytest

from iqa.components.brokers.artemis import Artemis
from iqa.instance import Instance

iqa_instance = Instance()


# def pytest_addoption(parser):
#     messaging_components = parser.getgroup('iqa-messaging_components')
#
#     # Broker master 1
#     messaging_components.addoption("--master1", action="append", default=['master1'])
#
#     # Broker slave 1
#     messaging_components.addoption("--slave1", action="append", default=['slave1'])
#
#     # Broker slave 2
#     messaging_components.addoption("--slave2", action="append", default=['slave2'])


def pytest_configure(config):
    # iqa_instance = IQAInstance(inventory=config.getvalue('inventory'))
    iqa_instance.inventory = config.getvalue('inventory')


#############################
# Section: Parametrization  #
#############################
#
# def pytest_generate_tests(metafunc):
#     """
#
#     """
#     if 'master1' in metafunc.fixturenames:
#         g_master1 = list(metafunc.config.option.sender)
#         metafunc.parametrize('master1', g_master1, indirect=True)
#
#     if 'slave1' in metafunc.fixturenames:
#         g_slave1 = list(metafunc.config.option.receiver)
#         metafunc.parametrize('slave1', g_slave1, indirect=True)
#
#     if 'slave2' in metafunc.fixturenames:
#         g_slave2 = list(metafunc.config.option.broker)
#         metafunc.parametrize('slave2', g_slave2, indirect=True)
#

########################
# Section: Fixtures    #
########################
node_master1 = iqa_instance.new_node(hostname='master1')
broker_master1 = iqa_instance.new_component(node=node_master1, component=Artemis)

node_slave1 = iqa_instance.new_node(hostname='slave1')
broker_slave1 = iqa_instance.new_component(node=node_slave1, component=Artemis)

node_slave2 = iqa_instance.new_node(hostname='slave2')
broker_slave2 = iqa_instance.new_component(node=node_slave2, component=Artemis)


@pytest.fixture()
def master1():
    """
    Map Artemis broker 1 component
    :return: Broker object
    """

    return broker_master1


@pytest.fixture()
def slave1():
    """
    Map Artemis broker 2 component
    :return: Broker object
    """

    return broker_slave1


@pytest.fixture()
def slave2():
    """
    Map Artemis broker 2 component
    :return: Broker object
    """

    return broker_slave2
