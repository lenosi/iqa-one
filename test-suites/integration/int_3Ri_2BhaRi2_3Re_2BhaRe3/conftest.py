from typing import Union

import pytest

from iqa.messaging.abstract.server.broker import Broker
from iqa.messaging.abstract.client import Sender, Receiver
from iqa.components.clients import \
    ReceiverJava, SenderJava, \
    ReceiverPython, SenderPython, \
    ReceiverNodeJS, SenderNodeJS
from iqa.components.routers.dispatch.dispatch import Dispatch
from iqa.pytest_iqa import IQAInstance


def pytest_addoption(parser):
    """
    This particular suite requires that the router1 ip address is informed,
    as it is used internally in the related inventory files.

    :param parser:
    :return:
    """

    parser.addoption("--msg-length", action="append", required=False, default=[1024],
                     help="Message length")


def pytest_generate_tests(metafunc):
    """
    Iterations for EdgeRouterMode02 test_suite
    """
    clients = [
        "java",
        "python",
        "nodejs",
    ]

    senders_comb = ['sender' + '_' + client for client in clients]
    receivers_comb = ['receiver' + '_' + client for client in clients]

    # Routers
    iqa: IQAInstance = metafunc.config.iqa
    routers = list()
    for router in iqa.routers:
        routers.append(router.node.hostname)

    # Broker queues
    broker_queues = ['brokeri2.durable.queue', 'brokeri2.nondurable.queue', 'brokere3.durable.queue',
                     'brokere3.nondurable.queue', 'interior.autolink.durable.queue',
                     'interior.autolink.nondurable.queue', 'edge.autolink.durable.queue',
                     'edge.autolink.nondurable.queue']

    # Address translation tuple
    address_translation_tuple = [
        ('addremoveprefix.durable.queue', 'brokeri2.durable.queue', 'Broker.M.I2'),
        ('durable.queue', 'brokeri2.durable.queue', 'Broker.M.I2'),
        ('removeprefix.brokeri2.durable.queue', 'brokeri2.durable.queue', 'Broker.M.I2'),
        ('edgeremove.durable.queue', 'brokere3.durable.queue', 'Broker.M.E3')
    ]
    address_translation_fixtures = ['address', 'translates_to', 'broker']

    # Broker durable topics
    broker_durable_topics = [
        ('brokeri2.durable.topic', 'Broker.M.I2'),
        ('brokere3.durable.topic', 'Broker.M.E3')
    ]
    # Broker non-durable topics
    broker_nondurable_topics = [
        ('brokeri2.nondurable.topic', 'Broker.M.I2'),
        ('brokere3.nondurable.topic', 'Broker.M.E3')
    ]

    if any([v for v in metafunc.fixturenames if v in ['sender', 'get_sender']]):
        metafunc.parametrize('sender', senders_comb, indirect=True)

    if any([v for v in metafunc.fixturenames if v in ['receiver', 'get_receiver']]):
        metafunc.parametrize('receiver', receivers_comb, indirect=True)

    if 'router' in metafunc.fixturenames:
        metafunc.parametrize('router', routers, indirect=True)

    if 'router_edge' in metafunc.fixturenames:
        metafunc.parametrize('router_edge', [r for r in routers if r.startswith('Router.E')], indirect=True)

    if 'router_interior' in metafunc.fixturenames:
        metafunc.parametrize('router_interior', [r for r in routers if r.startswith('Router.I')], indirect=True)

    if 'router_with_broker' in metafunc.fixturenames:
        metafunc.parametrize('router_with_broker', ['Router.I2', 'Router.E3'], indirect=True)

    if 'broker_master' in metafunc.fixturenames:
        metafunc.parametrize('broker_master', ['Broker.M.I2', 'Broker.M.E3'], indirect=True)

    if 'broker_slave' in metafunc.fixturenames:
        metafunc.parametrize('broker_slave', ['Broker.S.I2', 'Broker.S.E3'], indirect=True)

    if 'queue' in metafunc.fixturenames:
        metafunc.parametrize('queue', broker_queues)

    # If all fixture names defined in address_translation_fixtures exist in metafunc.fixturenames
    address_translation_fixtures_count = len([f for f in address_translation_fixtures if f in metafunc.fixturenames])
    if address_translation_fixtures_count == len(address_translation_fixtures):
        metafunc.parametrize('address,translates_to,broker', address_translation_tuple)

    if {'topic_durable', 'broker'}.issubset(metafunc.fixturenames):
            metafunc.parametrize('topic_durable,broker', broker_durable_topics)

    if {'topic_nondurable', 'broker'}.issubset(metafunc.fixturenames):
        metafunc.parametrize('topic_nondurable,broker', broker_nondurable_topics)


@pytest.fixture()
def router_e1(iqa) -> Dispatch:
    """
    Returns the router
    :param iqa:
    :return: Returns router instance
    """
    return iqa.get_routers('Router.E1')[0]


@pytest.fixture()
def router_e2(iqa) -> Dispatch:
    """
    Returns the router
    :param iqa:
    :return: Returns router instance
    """
    return iqa.get_routers('Router.E2')[0]


@pytest.fixture()
def router_e3(iqa) -> Dispatch:
    """
    Returns the router
    :param iqa:
    :return: Returns router instance
    """
    return iqa.get_routers('Router.E3')[0]


@pytest.fixture()
def router_i1(iqa) -> Dispatch:
    """
    Returns the router
    :param iqa:
    :return: Returns router instance
    """
    return iqa.get_routers('Router.I1')[0]


@pytest.fixture()
def router_i2(iqa) -> Dispatch:
    """
    Returns the router
    :param iqa:
    :return: Returns router instance
    """
    return iqa.get_routers('Router.I2')[0]


@pytest.fixture()
def router_i3(iqa) -> Dispatch:
    """
    Returns the router
    :param iqa:
    :return: Returns router instance
    """
    return iqa.get_routers('Router.I3')[0]


@pytest.fixture()
def broker_m_internal(iqa) -> Broker:
    """
    Returns the master broker instance connected to internal 2 router
    :param iqa:
    :return:
    """
    return iqa.get_brokers('Broker.M.I2')[0]


@pytest.fixture()
def broker_s_internal(iqa) -> Broker:
    """
    Returns the slave broker instance connected to internal 2 router
    :param iqa:
    :return:
    """
    return iqa.get_brokers('Broker.S.I2')[0]


@pytest.fixture()
def broker_m_edge(iqa) -> Broker:
    """
    Returns the master broker instance connected to edge 3 router
    :param iqa:
    :return:
    """
    return iqa.get_brokers('Broker.M.E3')[0]


@pytest.fixture()
def broker_s_edge(iqa) -> Broker:
    """
    Returns the slave broker instance connected to edge 3 router
    :param iqa:
    :return:
    """
    return iqa.get_brokers('Broker.S.E3')[0]


@pytest.fixture(name='get_sender')
def get_sender_(request, iqa):
    """
    Fixture of Sender Factory
    :param request:
    :param iqa:
    :return: Returns Sender Factory instance

    Example of usage:
    def test_two_senders(get_sender):
        sender1: Union[SenderJava, SenderPython, SenderNodeJS] = get_sender()
        sender2: Union[SenderJava, SenderPython, SenderNodeJS] = get_sender()
    """
    created = []

    def get_sender():
        if "sender_" in request.param:
            snd = request.param.split('_')
            sender_implementation = snd[1]
            sender = iqa.get_clients(Sender, sender_implementation)[0]
            created.append(sender)
            return sender

    yield get_sender

    for s in created:
        s.delete()


@pytest.fixture(name='get_receiver')
def get_receiver_(request, iqa):
    """
    Fixture of Receiver Factory
    :param request:
    :param iqa:
    :return: Returns Receiver Factory instance

    Example of usage:
    def test_two_receivers(get_receiver):
        receiver1: Union[SenderJava, SenderPython, SenderNodeJS] = get_receiver()
        receiver2: Union[SenderJava, SenderPython, SenderNodeJS] = get_receiver()
    """
    created = []

    def get_receiver():
        if "receiver_" in request.param:
            rcv: str = request.param.split('_')
            receiver_implementation = rcv[1]
            receiver = iqa.get_clients(Receiver, receiver_implementation)[0]
            created.append(receiver)
            return receiver

    yield get_receiver

    for r in created:
        r.delete()


@pytest.fixture
def receiver(request, iqa) -> Union[ReceiverJava, ReceiverPython, ReceiverNodeJS]:
    if "receiver_" in request.param:
        rcv: str = request.param.split('_')
        receiver_implementation = rcv[1]
        receiver = iqa.get_clients(Receiver, receiver_implementation)[0]
        return receiver


@pytest.fixture
def sender(request, iqa) -> Union[SenderJava, SenderPython, SenderNodeJS]:
    if "sender_" in request.param:
        snd = request.param.split('_')
        sender_implementation = snd[1]
        sender = iqa.get_clients(Sender, sender_implementation)[0]
        return sender


@pytest.fixture
def router_with_broker(request, iqa):
    if "Router." in request.param:
        router_hostname = request.param
        return iqa.get_routers(router_hostname)[0]


@pytest.fixture
def router(request, iqa):
    if "Router." in request.param:
        router_hostname = request.param
        return iqa.get_routers(router_hostname)[0]


@pytest.fixture
def router_edge(request, iqa):
    if "Router.E" in request.param:
        router_hostname = request.param
        return iqa.get_routers(router_hostname)[0]


@pytest.fixture
def router_interior(request, iqa):
    if "Router.I" in request.param:
        router_hostname = request.param
        return iqa.get_routers(router_hostname)[0]


@pytest.fixture
def broker_master(request, iqa):
    if "Broker.M." in request.param:
        broker_hostname = request.param
        return iqa.get_brokers(broker_hostname)[0]


@pytest.fixture
def broker_slave(request, iqa):
    if "Broker.S." in request.param:
        broker_hostname = request.param
        return iqa.get_brokers(broker_hostname)[0]

