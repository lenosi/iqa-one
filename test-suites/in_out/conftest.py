
import pytest


from iqa.components.clients.core.receiver import ReceiverCore
from iqa.components.clients.core.sender import SenderCore
from iqa.system.node import Node
from iqa.components.brokers.artemis import Artemis
from iqa.components.routers.dispatch import Dispatch


########################
# Section: Add option  #
########################

########################
# Section: Add option  #
########################


def pytest_addoption(parser):
    """

    :param parser:
    :return:
    """

    # Senders
    parser.addoption("--sender", action="append", default=[], help="Define which sender client")

    # Receivers
    parser.addoption("--receiver", action="append", default=[], help="Define which receiver client")

    # Routers
    parser.addoption("--router", action="append", default=[], help="Define which router [dispatch, interconnect]")

    # Brokers
    parser.addoption("--broker", action="append", default=[], help="Define which broker [amq7, artemis, rabitmq]")

    # In node
    parser.addoption("--in_node", action="store", default="localhost", help="node for ingress connection")

    # Out node
    parser.addoption("--out_node", action="store", default="localhost", help="node for egress connection")

    # Receiver node
    parser.addoption("--receiver_node", action="store", default="localhost", help="node where receiver is running")

    # Sender node
    parser.addoption("--sender_node", action="store", default="localhost", help="node where receiver is running")


#############################
# Section: Parametrization  #
#############################


def pytest_generate_tests(metafunc):
    if 'sender' in metafunc.fixturenames:
        senders = list(metafunc.config.option.sender)
        metafunc.parametrize('sender', senders, indirect=True)

    if 'receiver' in metafunc.fixturenames:
        receivers = list(metafunc.config.option.receiver)
        metafunc.parametrize('receiver', receivers, indirect=True)

    if 'broker' in metafunc.fixturenames:
        brokers = list(metafunc.config.option.broker)
        metafunc.parametrize('broker', brokers, indirect=True)

    if 'router' in metafunc.fixturenames:
        routers = list(metafunc.config.option.router)
        metafunc.parametrize('router', routers, indirect=True)


########################
# Section: Fixtures    #
########################


@pytest.fixture()
def sender(request):
    if 'native' in request.param:
        return SenderCore()


@pytest.fixture()
def receiver(request):
    if 'native' in request.param:
        return ReceiverCore()


@pytest.fixture()
def broker(request):
    broker_node = Node(hostname='ic01-r6i')
    if 'artemis' in request.param:
        return Artemis(node=broker_node)
    elif 'amq7' in request.param:
        return Artemis(node=broker_node)


@pytest.fixture()
def router(request):
    router_node = Node(hostname='ic01-r6i')
    if 'dispatch' in request.param:
        return Dispatch(node=router_node)
    elif 'interconnect' in request.param:
        return Dispatch(node=router_node)


@pytest.fixture()
def tls(request):
    if 'tls10' in request.param:
        return SenderCore()
    if 'tls11' in request.param:
        return SenderCore()
    if 'tls12' in request.param:
        return SenderCore()
    if 'tls13' in request.param:
        return SenderCore()


@pytest.fixture()
def sasl(request):
    """
    SASL Authentication fixture
    :param request:
    :return:
    """
    if 'sasl_user' in request.param and 'sasl_password':
        return None
    else:
        return None
