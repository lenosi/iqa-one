"""
Test address translation using the "address", "translates_to", "sender", "receiver", "broker"
and "router" fixtures:
- "address" fixture must provide an address to be used for exchanging messages.
- "translates_to" fixture must tell the final queue name (expected to exist on the broker)
- "sender" and "receiver" fixtures contain an instance of ClientExternal (for each valid implementation)
- "broker" fixture provides the broker instance where the queue is defined (used to query message count)
- "router" the router instance to connect when sending/receiving messages to/from
"""
import math
import hashlib
import logging
import ast
import time

import pytest

from iqa.components.brokers import Artemis, Broker
from iqa.instance.instance import Instance
from iqa.abstract.message import Message


class TestAddressTranslation(object):
    """
    Provides methods to test sending and receiving of messages using Address Translation
    through all routers available in the current topology. All final addresses must be
    valid queues defined on their respective broker instance.

    Notes:
        - MESSAGE_SIZE Should not exceed 256 (due to command line length limitations)
        - MESSAGE_BODY using only "integer" values is not working properly with RHEA sender
        - INCREASING SEND/RECV COUNT implicates in increasing TIMEOUT accordingly
    """
    # Tested sending 1000 and receiving 1000 (with a timeout of 600 - needed because of  the delay applied to I3 and E3)
    # Initial values must be kept low (10/1) till all engineering work is done, and then we must increase it properly.
    SEND_COUNT = 10
    RECV_COUNT = 1
    MESSAGE_SIZE = 128
    MESSAGE_BODY = (("ABCDEFGHIJKLMNOPQRSTUVWXYZ" * math.ceil(MESSAGE_SIZE / 10))[:MESSAGE_SIZE])
    # sha1 sum of message body (to validate integrity)
    MESSAGE_SHA1SUM = hashlib.sha1(MESSAGE_BODY.encode('utf-8')).hexdigest()

    # Must be defined considering the 200ms on Routers I3 and E3
    TIMEOUT = 60

    @staticmethod
    def _get_queue(broker, queue_name):
        """
        Loops through all queues in the given broker instance, returning
        the one that matches the provided queue name.
        :param broker:
        :param queue_name:
        :return:
        """
        for queue in broker.queues():
            if queue.name == queue_name:
                return queue
        return None

    def test_address_translation_sending(self, address, translates_to, sender, broker, router, iqa: Instance):
        """
        Send messages to the given "address", through the provided "router" instance. It uses the given
        "sender" (ClientExternal) instance and expects the queue with name "translates_to" to exist in
        the "broker" instance and that the number of messages in it will increase from initial message count
        to the value defined in the SEND_COUNT constant.
        :param address:
        :param translates_to:
        :param sender:
        :param broker:
        :param router:
        :param iqa:
        :return:
        """

        # if not router.node.hostname.startswith('Router.I'):
        #     return

        # Get broker instance for given broker name
        broker_instance: Broker = iqa.get_brokers(broker)[0]
        assert broker_instance

        # Retrieving current number of messages in the destination address (queue)
        queue = self._get_queue(broker_instance, translates_to)
        initial_message_count = int(queue.message_count)

        # Assert queue has been found
        assert queue
        assert initial_message_count is not None

        # Url to be used by senders and receivers
        url = "amqp://%s:%s/%s" % (router.node.get_ip(), router.port, address)

        # Preparing the external sender
        logging.info("Sending messages to %s - using %s" % (url, sender.implementation))
        sender.reset_command()
        sender.set_url(url)
        sender.command.control.count = self.SEND_COUNT
        sender.command.control.timeout = self.TIMEOUT  # Timeout flag for command to be executed
        sender.command.timeout = self.TIMEOUT  # Timeout for command (needed cause timeout flag is working properly)

        # Defining the message to be sent
        message = Message()
        message.body = self.MESSAGE_BODY

        # Sending and waiting for app to finish
        sender.send(message)
        sender.execution.wait()

        # Validating sender completed successfully
        logging.debug("Sender exit code: %s - timed out: %s" %
                      (sender.execution.returncode,
                       sender.execution.timed_out))
        assert sender.execution.completed_successfully()

        # Delaying 5 secs to clean up everything
        time.sleep(5)

        # Validates if all messages have been delivered
        queue = self._get_queue(broker_instance, translates_to)
        logging.info("Message count at queue %s - after senders completed = %s" % (translates_to, queue.message_count))
        assert (self.SEND_COUNT + initial_message_count) == int(queue.message_count)

    def test_address_translation_receiving(self, address, translates_to, receiver, broker, router, iqa: Instance):
        """
        Receive messages from the provided "address" connecting with the "router" instance.
        This test will execute an external client using the "receiver" instance and expect it to
        consume RECV_COUNT messages from the given "address". The "address" used for receiving should resolve
        as the "translates_to" value, which must be a queue name on the "broker" instance.
        The number of messages in the respective queue must be equals or greater than RECV_COUNT.
        This test will validate number of received messages as well as perform an SHA1 sum based
        on the message's body, which must match the generated SHA1 sum from message sent earlier.
        :param address:
        :param translates_to:
        :param receiver:
        :param broker:
        :param router:
        :param iqa:
        :return:
        """

        # if not router.node.hostname.startswith('Router.I'):
        #     return

        # Get broker instance for given broker name
        broker_instance: Broker = iqa.get_brokers(broker)[0]
        assert broker_instance

        # Retrieving current number of messages in the destination address (queue)
        queue = self._get_queue(broker_instance, translates_to)
        initial_message_count = int(queue.message_count)
        logging.info("Initial message count at queue %s - after receivers completed = %s"
                     % (translates_to, queue.message_count))

        # Assert queue has been found and senders were able to send something
        assert queue
        assert initial_message_count >= self.RECV_COUNT

        # Url to be used by receivers
        url = "amqp://%s:%s/%s" % (router.node.get_ip(), router.port, address)

        # Preparing receiver
        logging.info("Receiving messages from %s - using %s" % (url, receiver.implementation))
        receiver.reset_command()
        receiver.set_url(url)
        receiver.command.control.count = self.RECV_COUNT
        # cannot be used with cli-rhea as it is "waiting" for the given amount of time (causing a timeout to happen)
        if receiver.implementation != 'nodejs':
            receiver.command.control.timeout = self.TIMEOUT  # Timeout flag for command to be executed
        receiver.command.logging.log_msgs = 'dict'
        receiver.command.timeout = self.TIMEOUT  # Timeout for command

        # Executes external receiver and waits until it finishes (or times out)
        receiver.receive()
        receiver.execution.wait()

        # Validating results
        logging.info("Receiver exit code: %s - timed out: %s" %
                     (receiver.execution.returncode,
                      receiver.execution.timed_out))
        assert receiver.execution.completed_successfully()

        # Validating message integrity
        stdout_lines = receiver.execution.read_stdout(lines=True)
        assert len(stdout_lines) == self.RECV_COUNT

        # Reading each message body and comparing SHA1 sum
        for recv_msg in stdout_lines:
            # Failing if a blank line was received
            if not recv_msg:
                pytest.fail("Not expecting an empty message")
                continue
            try:
                recv_msg_dict = ast.literal_eval(recv_msg)
            except ValueError:
                pytest.fail("Invalid message body returned. Expecting a dict.")

            # Failing if invalid content received from external client
            if 'content' not in recv_msg_dict.keys():
                pytest.fail('Expecting a content element as part of message dict.')
                continue

            # Failing if message returned with empty body
            body = recv_msg_dict['content']
            if not body:
                pytest.fail("No message body available")
                continue

            # Validate integrity
            assert hashlib.sha1(body.encode('utf-8')).hexdigest() == self.MESSAGE_SHA1SUM

        # Delaying 5 secs to clean up everything
        time.sleep(5)

        # Validates if all messages have been received
        queue = self._get_queue(broker_instance, translates_to)
        logging.info("Message count at queue %s - after receivers completed = %s"
                     % (translates_to, queue.message_count))
        assert (initial_message_count - self.RECV_COUNT) == int(queue.message_count)
