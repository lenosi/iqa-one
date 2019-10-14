# Initial static configuration
from iqa.abstract.message import Message
from iqa.components.clients import \
    ReceiverJava, SenderJava, \
    ReceiverPython, SenderPython, \
    ReceiverNodeJS, SenderNodeJS
import logging

MESSAGE_COUNT = 10
MESH_SIZE = 3

logger = logging.getLogger(__name__)


def test_basic_messaging(
        receiver: [ReceiverJava, ReceiverPython, ReceiverNodeJS],
        sender: [SenderJava, SenderPython, SenderNodeJS],
        msg_length: [int]):
    """
    Exchange messages through the router using a pair of Java Sender and Receiver.
    Expects that all messages are exchanged and external clients complete successfully.
    :param receiver:
    :param sender:
    :param msg_length:
    :return:
    """
    exchange_messages(receiver, sender, msg_length)
    validate_client_results(receiver, sender)


def start_receiver(receiver: [ReceiverJava, ReceiverPython, ReceiverNodeJS]):
    """
    Starts the provided receiver instance using pre-defined message count (per implementation)
    and sets it to log received messages as a dictionary (one message per line).
    :param receiver:
    :return:
    """
    # Defining number of messages to exchange
    receiver.command.control.count = MESSAGE_COUNT
    receiver.command.logging.log_msgs = 'dict'
    receiver.command.stdout = True
    receiver.command.stderr = True

    # Starting the Receiver
    logger.info("Starting receiver: [implementation=%s | message count=%s | timeout=%s" % (
                receiver.implementation,
                receiver.command.control.count,
                receiver.command.control.timeout))
    receiver.receive()


def start_sender(sender: [SenderJava, SenderPython, SenderNodeJS], length: int):
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
    sender.command.control.count = MESSAGE_COUNT
    sender.command.stdout = True
    sender.command.stderr = True

    # Starting the Sender
    message = Message(body="X" * length)
    logger.info("Starting sender: [implementation=%s | message count=%s | timeout=%s" % (
                sender.implementation,
                sender.command.control.count,
                sender.command.control.timeout))
    sender.send(message)


def exchange_messages(receiver: [ReceiverJava, ReceiverPython, ReceiverNodeJS],
                      sender: [SenderJava, SenderPython, SenderNodeJS],
                      length):
    """
    Starts both receiver and sender (with message sizes set to appropriate length).
    :param receiver:
    :param sender:
    :param length:
    :return:
    """
    start_receiver(receiver)
    start_sender(sender, length)


def validate_client_results(receiver: [ReceiverJava, ReceiverPython, ReceiverNodeJS],
                            sender: [SenderJava, SenderPython, SenderNodeJS]):
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
    import time
    logger.info('Waiting on receiver and sender to complete (or timeout)')
    while receiver.execution.is_running() or sender.execution.is_running():
        time.sleep(0.1)

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
    assert len(receiver.execution.read_stdout(lines=True)) >= MESSAGE_COUNT

    # Validating if sender process completed without timing out
    assert not sender.execution.is_running()
    assert sender.execution.returncode == 0, \
        '%s did not complete successfully' % sender.implementation.upper()
