from typing import List

from iqa.system.executor import Execution
from iqa.system.command.command_base import Command
from iqa.abstract.message.message import Message
from iqa.components.clients.external.java.receiver import ReceiverJava
from iqa.components.clients.external.java.sender import SenderJava
from iqa.components.clients.external.python.receiver import ReceiverPython
from iqa.components.clients.external.python.sender import SenderPython
from iqa.components.clients.external.nodejs.receiver import ReceiverNodeJS
from iqa.components.clients.external.nodejs.sender import SenderNodeJS
from iqa.utils.types import ReceiverType, SenderType, RouterType

# Initial static configuration
from iqa.components.routers.dispatch.dispatch import Dispatch
from iqa.components.routers.dispatch.management.query import RouterQuery
from iqa.instance.instance import Instance
import time
import logging


# TODO Java sender is working very slowly (need to discuss with clients team)
WAIT_ROUTER_MESH_SECS: int = 90
MESH_SIZE: int = 3
MESSAGE_COUNT: dict = {'java': 10, 'python': 100, 'nodejs': 100}
TIMEOUT: int = 120
logger: logging.Logger = logging.getLogger(__name__)


def test_scale_up_router(router: Dispatch) -> None:
    """
    Executes "oc" command to scale up the number of PODs according to value defined in MESH_SIZE constant.
    It also uses 'amq-interconnect' as the deployment config name (standard in official templates).

    Test passes if command is executed without errors.
    Note: the oc command expects that current session is logged to Openshift cluster (you can do it manually,
          but it will be also done through the CI job).
    :param router:
    :return:
    """
    cmd_scale_up: Command = Command(args=['oc', 'scale', '--replicas=%d' % MESH_SIZE, 'dc', 'amq-interconnect'],
                                    timeout=TIMEOUT, stderr=True, stdout=True)
    execution: Execution = router.node.execute(cmd_scale_up)
    execution.wait()

    # If debug enabled, logging stdout (or stderr when using local executor)
    if logger.isEnabledFor(logging.DEBUG) and not execution.completed_successfully():
        logger.debug("Scale up has failed, stdout: %s" % (execution.read_stdout()))

    assert execution.completed_successfully()


def test_router_mesh_after_scale_up(router: Dispatch) -> None:
    """
    Queries Router for all Node Entities available in the topology.
    It expects the number of nodes matches number of PODs (mesh is correctly formed).
    :param router:
    :return:
    """
    assert router
    validate_mesh_size(router, MESH_SIZE)


def test_basic_messaging_with_java(java_receiver: ReceiverJava, java_sender: SenderJava, length: int) -> None:
    """
    Exchange messages through the router using a pair of Java Sender and Receiver.
    Expects that all messages are exchanged and external clients complete successfully.
    :param java_receiver:
    :param java_sender:
    :param length:
    :return:
    """
    exchange_messages(java_receiver, java_sender, length)
    validate_client_results(java_receiver, java_sender)


def test_basic_messaging_with_python(python_receiver: ReceiverPython, python_sender: SenderPython, length: int) -> None:
    """
    Exchange messages through the router using a pair of Python Sender and Receiver.
    Expects that all messages are exchanged and external clients complete successfully.
    :param python_receiver:
    :param python_sender:
    :param length:
    :return:
    """
    exchange_messages(python_receiver, python_sender, length)
    validate_client_results(python_receiver, python_sender)


def test_basic_messaging_with_nodejs(nodejs_receiver: ReceiverNodeJS, nodejs_sender: SenderNodeJS, length: int) -> None:
    """
    Exchange messages through the router using a pair of NodeJS Sender and Receiver.
    Expects that all messages are exchanged and external clients complete successfully.
    :param nodejs_receiver:
    :param nodejs_sender:
    :param length:
    :return:
    """
    exchange_messages(nodejs_receiver, nodejs_sender, length)
    validate_client_results(nodejs_receiver, nodejs_sender)


def test_basic_messaging_with_all_clients_concurrently(iqa: Instance, length: int) -> None:
    """
    Exchange messages through the router using three pairs of:
    - Java Sender and Receiver
    - Python Sender and Receiver, and
    - NodeJS Sender and Receiver.
    Expects that all messages are exchanged and all external clients complete successfully.
    :param iqa:
    :param length:
    :return:
    """

    receivers: List[ReceiverType] = iqa.get_clients(client_type=ReceiverType)
    senders: List[SenderType] = iqa.get_clients(client_type=SenderType)

    # Run all available clients in parallel
    for receiver in receivers:
        start_receiver(receiver)
    for sender in senders:
        start_sender(sender, length)

    # Validate all results
    for receiver, sender in zip(receivers, senders):
        validate_client_results(receiver, sender)


def test_scale_down_router(router: Dispatch) -> None:
    """
    Scale down the number of PODs to 1.
    Expects that the scale down command completes successfully.
    :param router:
    :return:
    """
    cmd_scale_up: Command = Command(args=['oc', 'scale', '--replicas=1', 'dc', 'amq-interconnect'], timeout=TIMEOUT)
    execution: Execution = router.node.execute(cmd_scale_up)
    execution.wait()

    # If debug enabled, logging stdout (or stderr when using local executor)
    if logger.isEnabledFor(logging.DEBUG) and not execution.completed_successfully():
        logger.debug("Scale down has failed, stdout: %s" % (execution.read_stdout()))

    assert execution.completed_successfully()


def test_router_mesh_after_scale_down(router: Dispatch) -> None:
    """
    Queries the router to validate that the number of Nodes in the topology is 1.
    :param router:
    :return:
    """
    assert router
    validate_mesh_size(router, 1)


def validate_mesh_size(router: RouterType, new_size: int) -> None:
    """
    Asserts that router topology size matches "new_size" value.
    :param router:
    :param new_size:
    :return:
    """
    # Wait before querying nodes
    logger.debug('Waiting %s seconds for router mesh to be formed' % WAIT_ROUTER_MESH_SECS)
    time.sleep(WAIT_ROUTER_MESH_SECS)

    # Query nodes in topology
    query: RouterQuery = RouterQuery(host=router.node.ip, port=router.port, router=router)
    node_list: list = query.node()
    logging.debug("List of nodes: %s" % node_list)

    # Assertions
    assert node_list
    assert len(node_list) == new_size


def start_receiver(receiver: ReceiverType) -> None:
    """
    Starts the provided receiver instance using pre-defined message count (per implementation)
    and sets it to log received messages as a dictionary (one message per line).
    :param receiver:
    :return:
    """
    assert receiver

    # Defining number of messages to exchange
    receiver.command.control.count = MESSAGE_COUNT.get(receiver.implementation)
    receiver.command.logging.log_msgs = 'dict'
    receiver.command.stdout = True
    receiver.command.stderr = True

    # Starting the Receiver
    logger.info("Starting receiver: [implementation=%s | message count=%s | timeout=%s" % (
                receiver.implementation,
                receiver.command.control.count,
                receiver.command.control.timeout))
    receiver.receive()


def start_sender(sender: SenderType, length: int) -> None:
    """
    Starts the sender instance, preparing a dummy message whose body size has
    the provided length.

    Currently message content is passed via command line.
    TODO: We must enhance our clients to generate a temporary file (on the executing node)
          and use the related file as input for message content.
    :param sender:
    :param length:
    :return:
    """
    assert sender

    sender.command.control.count = MESSAGE_COUNT.get(sender.implementation)
    sender.command.timeout = TIMEOUT
    sender.command.stdout = True
    sender.command.stderr = True

    # Starting the Sender
    message = Message(body="X" * length)

    logger.info("Starting sender: [implementation=%s | message count=%s | timeout=%s" % (
                sender.implementation,
                sender.command.control.count,
                sender.command.control.timeout))
    sender.send(message)


def exchange_messages(receiver: ReceiverType, sender: SenderType, length: int) -> None:
    """
    Starts both receiver and sender (with message sizes set to appropriate length).
    :param receiver:
    :param sender:
    :param length:
    :return:
    """
    start_receiver(receiver)
    start_sender(sender, length)


def validate_client_results(receiver: ReceiverType, sender: SenderType) -> None:
    """
    Validate that both clients completed (or timed out) and if the
    number of messages received by receiver instance matches
    expected count.
    :param receiver:
    :param sender:
    :return:
    """
    #
    # Validating results
    #
    # Wait till both processes complete
    logger.info('Waiting on receiver and sender to complete (or timeout)')
    while receiver.execution.is_running() or sender.execution.is_running():
        pass

    # Debugging receiver results
    if not receiver.execution.completed_successfully():
        logger.debug("Receiver did not complete successfully [exit code = %d]"
                     % receiver.execution.returncode)
        logger.debug("Receiver stdout = %s" % receiver.execution.read_stdout())
        logger.debug("Receiver stderr = %s" % receiver.execution.read_stderr())

    # Debugging sender results
    if not sender.execution.completed_successfully():
        logger.debug("Sender did not complete successfully [exit code = %d]"
                     % sender.execution.returncode)
        logger.debug("Sender stdout = %s" % sender.execution.read_stdout())
        logger.debug("Sender stderr = %s" % sender.execution.read_stderr())

    # Validating receiver results
    assert not receiver.execution.is_running()
    assert receiver.execution.returncode == 0, \
        '%s did not complete successfully' % receiver.implementation.upper()

    # Each message received will be printed as one line (plus some extra lines from Ansible)
    assert len(receiver.execution.read_stdout(lines=True)) >= MESSAGE_COUNT.get(receiver.implementation)

    # Validating if sender process completed without timing out
    assert not sender.execution.is_running()
    assert sender.execution.returncode == 0, \
        '%s did not complete successfully' % sender.implementation.upper()
