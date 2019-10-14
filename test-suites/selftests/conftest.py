import pytest

# from messaging_components import clients, routers, brokers
from iqa.components.clients.external import nodejs, python
from iqa.components.clients.core.receiver import ReceiverCore
from iqa.components.clients.core.sender import SenderCore
from iqa.components.brokers.artemis import Artemis
from iqa.components.routers.dispatch import Dispatch

from iqa.instance.instance import Instance

from iqa.pytest.fixtures import iqa as pytest_iqa


############################
# Global python namespace  #
############################
iqa_instance = Instance()


def pytest_namespace():
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
def pytest_addoption(parser):
    """
    Add messaging options to py.test runner
    """
    components = parser.getgroup('iqa-messaging_components')

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


def pytest_configure(config):
    """into iqa instance"""
    pytest_iqa.inventory = config.option.inventory
    # pytest.iqa.inventory = config.option.inventory
    # iqa_instance.inventory = config.option.inventory


##############################
# Section: Parametrization  #
#############################
def pytest_generate_tests(metafunc):
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

broker_node = iqa_instance.new_node(hostname='ic01')
router_node = iqa_instance.new_node(hostname='ic01')
client_node = iqa_instance.new_node(hostname='ic01')

core_sender = SenderCore()
core_receiver = ReceiverCore()

nodejs_sender = iqa_instance.new_component(node=client_node, component=nodejs.Sender)
nodejs_receiver = iqa_instance.new_component(node=client_node, component=nodejs.Receiver)

python_sender = iqa_instance.new_component(node=client_node, component=python.SenderPython)
python_receiver = iqa_instance.new_component(node=client_node, component=python.ReceiverPython)

amq6 = iqa_instance.new_component(node=broker_node, component=Artemis)
amq7 = iqa_instance.new_component(node=broker_node, component=Artemis)
artemis = iqa_instance.new_component(node=broker_node, component=Artemis)

dispatch = iqa_instance.new_component(node=router_node, component=Dispatch)


@pytest.fixture()
def sender(request):
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
def receiver(request):
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
def broker(request):
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
def router(request):
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
def tls(request):
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
