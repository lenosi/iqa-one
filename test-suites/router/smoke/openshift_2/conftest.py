import pytest
import itertools
from typing import Union, Tuple, Type

from _pytest.config.argparsing import Parser
from _pytest.python import Metafunc

from iqa.components.clients.external.java.receiver import ReceiverJava
from iqa.components.clients.external.java.sender import SenderJava
from iqa.components.clients.external.python.receiver import ReceiverPython
from iqa.components.clients.external.python.sender import SenderPython
from iqa.components.clients.external.nodejs.receiver import ReceiverNodeJS
from iqa.components.clients.external.nodejs.sender import SenderNodeJS
from iqa.components.routers.dispatch.dispatch import Dispatch

from iqa.abstract.client.receiver import Receiver
from iqa.abstract.client.sender import Sender
from iqa.instance.instance import Instance
from iqa.utils.types import ReceiverType, SenderType

clients: list = [
    "java",
    "python",
    "nodejs",
]


def pytest_addoption(parser: Parser) -> None:
    """
    This particular suite requires that the router1 ip address is informed,
    as it is used internally in the related inventory files.

    :param parser:
    :return:
    """

    parser.addoption("--cluster", action="append", required=True,
                     help="Openshift clusters IP where routers is deployed")

    parser.addoption("--token", action="append", required=True,
                     help="Token to authenticate with OCP same order as --cluster")

    parser.addoption("--msg-length", action="append", required=False, default=[256],
                     help="Message length")


def pytest_generate_tests(metafunc: Metafunc) -> None:
    """
    Iterate through tests with length parameter and make
    sure tests will be executed with 1024 increment.
    """

    clusters: list = list(metafunc.config.option.cluster)
    clusters_count: int = len(clusters)
    clients_cluster: list = [client + '_' + str(cluster) for client, cluster
                             in itertools.product(clients, range(0, clusters_count))]

    routers: list = ['router' + '_' + str(cluster) for cluster in range(0, clusters_count)]
    senders: list = ['sender' + '_' + client for client in clients_cluster]
    receivers: list = ['receiver' + '_' + client for client in clients_cluster]

    if 'msg_length' in metafunc.fixturenames:
        # metafunc.parametrize("msg_length", [2 ** x for x in range(8, 15)])
        msg_lengths: list = list(metafunc.config.option.msg_length)
        metafunc.parametrize("msg_length", msg_lengths)

    if 'sender' in metafunc.fixturenames:
        metafunc.parametrize('sender', senders, indirect=True)

    if 'receiver' in metafunc.fixturenames:
        metafunc.parametrize('receiver', receivers, indirect=True)

    if 'router_cluster' in metafunc.fixturenames:
        metafunc.parametrize('router_cluster', routers, indirect=True)


@pytest.fixture()
def receiver(request, iqa: Instance) -> Union[ReceiverJava, ReceiverPython, ReceiverNodeJS]:
    """
    Fixture the first Receiver instance
    :param request:
    :param iqa:
    :return: Returns first Receiver instance on 1 cluster instance
    """
    if "receiver_" in request.param:
        s: list = request.param.split('_')
        receiver_implementation: str = s[1]
        receiver_number: int = int(s[2])
        receiver: ReceiverType = iqa.get_clients(Type[Receiver], receiver_implementation)[0]
        receiver.set_url("amqp://%s:5672/address" % request.config.option.cluster[receiver_number])
        return receiver


@pytest.fixture()
def sender(request, iqa: Instance) -> Union[SenderJava, SenderPython, SenderNodeJS]:
    """
    Fixture the first Sender instance
    :param request:
    :param iqa:
    :return: Returns first Sender instance on 1 cluster instance
    """
    if "sender_" in request.param:
        s: list = request.param.split('_')
        sender_implementation: str = s[1]
        sender_number: int = int(s[2])
        sender: SenderType = iqa.get_clients(Type[Sender], sender_implementation)[0]
        sender.set_url("amqp://%s:5672/address" % request.config.option.cluster[sender_number])
        return sender


@pytest.fixture()
def router_cluster(request, iqa: Instance) -> Tuple[Dispatch, str, str]:
    """
    Returns the router, cluster and token from parameter
    :param request:
    :param iqa:
    :return: Returns router instance based on parametrized info
    """
    if 'router_' in request.param:
        router_number: int = int(request.param.split('_')[1])
        return (iqa.get_routers()[router_number],
                request.config.option.cluster[router_number],
                request.config.option.token[router_number])
