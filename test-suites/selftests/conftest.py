from typing import Dict, Union

import pytest

from _pytest.config import Config
from _pytest.config.argparsing import Parser, OptionGroup
from _pytest.python import Metafunc

from iqa.components.clients.external.nodejs.sender import SenderNodeJS
from iqa.components.clients.external.nodejs.receiver import ReceiverNodeJS
from iqa.components.clients.external.python.sender import SenderPython
from iqa.components.clients.external.python.receiver import ReceiverPython
from iqa.components.clients.core.receiver import ReceiverCore
from iqa.components.clients.core.sender import SenderCore
from iqa.components.brokers.artemis.artemis import Artemis
from iqa.components.routers.dispatch.dispatch import Dispatch

from iqa.instance.instance import Instance

from iqa.system.executor import Executor
from iqa.system.node.node import Node
from iqa.system.service import Service

from iqa.pytest.fixtures import iqa as pytest_iqa


############################
# Global python namespace  #
############################

iqa_instance: Instance = Instance()


def pytest_namespace() -> Dict[str, Instance]:
    """
    Provide iqa_instance to pytest global namespace
    """
    return {'iqa': iqa_instance}


@pytest.fixture
def iqa():
    """
    IQA instance with accessible node, messaging_components
    :return:
    """
    # return pytest.iqa
    return pytest_iqa


########################
# Section: Add option  #
########################
def pytest_addoption(parser: Parser) -> None:
    """
    Add messaging options to py.test runner
    """
    components: OptionGroup = parser.getgroup('iqa-messaging_components')

    # Senders
    components.addoption("--sender", action="append", default=[], help="Define sender client [native, nodejs]")

    # Brokers
    components.addoption("--receiver", action="append", default=[], help="Define receiver client []")

    # Routers
    components.addoption("--router", action="append", default=[], help="Define which router [dispatch, interconnect]")

    # Brokers
    components.addoption("--broker", action="append", default=[], help="Define which broker [amq7, artemis, rabitmq]")

    # TLS
    components.addoption("--tls", action="append", default=[], help="TLS option [tls10,tls11,tls12,tls13]")


def pytest_configure(config: Config) -> None:
    """into iqa instance"""
    pytest_iqa.inventory = config.option.inventory
    # pytest.iqa.inventory = config.option.inventory
    # iqa_instance.inventory = config.option.inventory


##############################
# Section: Parametrization  #
#############################
def pytest_generate_tests(metafunc: Metafunc) -> None:
    """
    Generate clients, brokers, matrix
    :param metafunc:
    :return:
    """
    if 'sender' in metafunc.fixturenames:
        g_senders = list(metafunc.config.option.sender)
        metafunc.parametrize('sender', g_senders, indirect=True)

    if 'receiver' in metafunc.fixturenames:
        g_receivers = list(metafunc.config.option.receiver)
        metafunc.parametrize('receiver', g_receivers, indirect=True)

    if 'broker' in metafunc.fixturenames:
        g_brokers = list(metafunc.config.option.broker)
        metafunc.parametrize('broker', g_brokers, indirect=True)

    if 'router' in metafunc.fixturenames:
        g_routers = list(metafunc.config.option.router)
        metafunc.parametrize('router', g_routers, indirect=True)

    if 'tls' in metafunc.fixturenames:
        g_tls = list(metafunc.config.option.tls)
        metafunc.parametrize('tls', g_tls, indirect=True)


########################
# Section: Fixtures    #
########################

broker_node: Node = iqa_instance.new_node(hostname='ic01')
router_node: Node = iqa_instance.new_node(hostname='ic01')
client_node: Node = iqa_instance.new_node(hostname='ic01')

core_sender: SenderCore = SenderCore(name='sender_core', node=client_node)
core_receiver: ReceiverCore = ReceiverCore(name='receiver_core', node=client_node)

nodejs_sender_component: SenderNodeJS = SenderNodeJS(name='sender_nodejs', node=client_node)
nodejs_sender: SenderNodeJS = iqa_instance.new_component(component=nodejs_sender_component)

nodejs_receiver_component: ReceiverNodeJS = ReceiverNodeJS(name='receiver_nodejs', node=client_node)
nodejs_receiver: ReceiverNodeJS = iqa_instance.new_component(component=nodejs_receiver_component)

python_sender_component: SenderPython = SenderPython(name='sender_python', node=client_node)
python_sender: SenderPython = iqa_instance.new_component(component=python_sender_component)

python_receiver_component: ReceiverPython = ReceiverPython(name='receiver_python', node=client_node)
python_receiver: ReceiverPython = iqa_instance.new_component(component=python_receiver_component)

artemis_component: Artemis = Artemis(name='artemis', node=broker_node)
amq6: Artemis = iqa_instance.new_component(component=artemis_component)
amq7: Artemis = iqa_instance.new_component(component=artemis_component)
artemis: Artemis = iqa_instance.new_component(component=artemis_component)

dispatch_node: Node = iqa_instance.new_node(hostname='ic01')
dispatch_service: Service = Service(name='dispatch_service', executor=Executor())
dispatch_component: Dispatch = Dispatch(name='disp', node=dispatch_node, service=dispatch_service)
dispatch: Dispatch = iqa_instance.new_component(component=dispatch_component)


@pytest.fixture()
def sender(request) -> Union[SenderCore, SenderNodeJS, SenderPython]:
    """
    Sender fixture client
    :param request:
    :return:
    """
    if 'native' in request.param:
        return core_sender
    elif 'nodejs' in request.param:
        return nodejs_sender
    elif 'python' in request.param:
        return python_sender


@pytest.fixture()
def receiver(request) -> Union[ReceiverCore, ReceiverNodeJS, ReceiverPython]:
    """
    Receiver fixture client
    :param request:
    :return:
    """
    if 'native' in request.param:
        return core_receiver
    elif 'nodejs' in request.param:
        return nodejs_receiver
    elif 'python' in request.param:
        return python_receiver


@pytest.fixture()
def broker(request) -> Artemis:
    """
    Iteration objects for broker
    :return: Broker object
    """

    if 'artemis' in request.param:
        return artemis
    elif 'amq7' in request.param:
        return artemis
    elif 'amq6' in request.param:
        return artemis


@pytest.fixture()
def router(request) -> Dispatch:
    """
    Iteration objects for router
    :param request:
    :return: Router object
    """
    if 'dispatch' in request.param:
        return dispatch
    elif 'interconnect' in request.param:
        return dispatch


@pytest.fixture()
def tls(request) -> str:
    """
    Iteration object for TLS settings
    :param request:
    :return:
    """
    if 'tls10' in request.param:
        return 'settings for tls10'
    elif 'tls11' in request.param:
        return 'settings for tls11'
    elif 'tls12' in request.param:
        return 'settings for tls12'
    elif 'tls13' in request.param:
        return 'settings for tls13'


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
