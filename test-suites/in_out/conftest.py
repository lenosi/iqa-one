import pytest
from _pytest.config.argparsing import Parser
from _pytest.python import Metafunc

from iqa.components.brokers.artemis.artemis import Artemis
from iqa.components.routers.dispatch.dispatch import Dispatch
from iqa.components.clients.core.receiver import ReceiverCore
from iqa.components.clients.core.sender import SenderCore
from iqa.instance.instance import Instance
from iqa.system.executor import ExecutorBase
from iqa.system.node.node import Node
from iqa.system.service import Service

iqa_instance: Instance = Instance()

########################
# Section: Add option  #
########################

########################
# Section: Add option  #
########################


def pytest_addoption(parser: Parser) -> None:
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


def pytest_generate_tests(metafunc: Metafunc) -> None:
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
client_node: Node = iqa_instance.new_node(hostname='ic01')

executor: ExecutorBase = ExecutorBase()

dispatch_service: Service = Service(name='dispatch_service', executor=executor)


@pytest.fixture()
def sender(request) -> SenderCore:
    if 'native' in request.param:
        return SenderCore(name='sender_core', node=client_node)


@pytest.fixture()
def receiver(request) -> ReceiverCore:
    if 'native' in request.param:
        return ReceiverCore(name='receiver_core', node=client_node)


@pytest.fixture()
def broker(request) -> Artemis:
    broker_node: Node = Node(hostname='ic01-r6i', executor=executor)
    if 'artemis' in request.param:
        return Artemis(name='artemis', node=broker_node)
    elif 'amq7' in request.param:
        return Artemis(name='amq7', node=broker_node)


@pytest.fixture()
def router(request) -> Dispatch:
    router_node: Node = Node(hostname='ic01-r6i', executor=executor)
    if 'dispatch' in request.param:
        return Dispatch(name='dispatch', node=router_node, service=dispatch_service)
    elif 'interconnect' in request.param:
        return Dispatch(name='interconnect', node=router_node, service=dispatch_service)


@pytest.fixture()
def tls(request) -> SenderCore:
    if 'tls10' in request.param:
        return SenderCore(name='tls1.0', node=client_node)
    if 'tls11' in request.param:
        return SenderCore(name='tls1.1', node=client_node)
    if 'tls12' in request.param:
        return SenderCore(name='tls1.2', node=client_node)
    if 'tls13' in request.param:
        return SenderCore(name='tls1.3', node=client_node)


@pytest.fixture()
def sasl(request) -> None:
    """
    SASL Authentication fixture
    :param request:
    :return:
    """
    if 'sasl_user' in request.param and 'sasl_password':
        return None
    else:
        return None
