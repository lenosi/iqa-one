import hashlib
import time

from iqa.instance.instance import Instance

from integration.int_3Ri_2BhaRi2_3Re_2BhaRe3.receiver import Receiver
from integration.int_3Ri_2BhaRi2_3Re_2BhaRe3.sender import Sender

"""
Test that validates Durable/Non-durable subscription using addresses that
flow through link-routes in the Dispatch Routers.
This class provides tests to validate synchronous and asynchronous behavior when
using Durable vs Non-durable subscriptions through the Router (and reaching
multi-cast addresses/queues in the Broker).
"""


class TestDurableNonDurableSubscription(object):

    MESSAGES = 1000
    MESSAGE_SIZE = 128
    TIMEOUT = 600
    DELAY = 5

    @staticmethod
    def _get_router_url(router, topic):
        """
        Returns an "amqp" url to connect with the given router / topic
        :param router:
        :param topic:
        :rtype: str
        :return:
        """
        return "amqp://%s:%s/%s" % (router.node.get_ip(), router.port, topic)

    def create_publishers(self, routers, topic):
        """
        Returns a list of Publisher (sender) threads (already started) to
        send messages through the given router/topic (address).
        The Sender will be initialized with the constants defined through this
        class.
        :param routers:
        :param topic:
        :rtype: list of Sender(Thread) objects - already started
        :return:
        """
        # Starting publishers
        publishers = list()

        for router in routers:
            publisher = Sender(url=self._get_router_url(router, topic),
                               message_count=self.MESSAGES,
                               sender_id='sender-%s' % router.node.hostname,
                               timeout=self.TIMEOUT,
                               message_size=self.MESSAGE_SIZE,
                               use_unique_body=True)
            publishers.append(publisher)

            # Starting publisher
            publisher.start()

        return publishers

    def create_subscribers(self, routers, topic, durable, timeout=None):
        """
        Returns a list of Subscriber (receiver) threads (already started) to
        receive messages from the given router/topic (address).
        The Receiver will be initialized with the constants defined through this
        class.
        :param routers:
        :param topic:
        :param durable:
        :param timeout:
        :rtype: list of Receiver(Thread) objects - already started
        :return:
        """

        # List of subscribers and subscribers
        subscribers = list()

        # Creating durable subscriptions across all routers
        container_id = None

        for router in routers:
            if durable:
                container_id = 'receiver-%s' % router.node.hostname

            subscriber = Receiver(url=self._get_router_url(router, topic),
                                  message_count=self.MESSAGES * len(routers),
                                  timeout=timeout or self.TIMEOUT,
                                  container_id=container_id,
                                  durable=durable,
                                  save_messages=True)
            subscribers.append(subscriber)

            # Starting subscriber
            subscriber.start()

        return subscribers

    def validate_all_messages_received(self, sent_body, routers, subscribers):
        """
        Common validation for test cases where receivers are expected to
        receive a pre-defined amount of messages. The following validations
        are performed:
        - Each receiver in the provided subscriber list, received self.MESSAGES * len(routers)
          (pre-defined amount of messages times number of routers in the topology)
        - Subscriber list cannot be empty
        - Each subscriber in the list must have a list with all message bodies received
        - If performs an SHA1 sum of each received body and compares it with the SHA1 for
          the unique message body sent by all senders
        :param sent_body:
        :param routers:
        :param subscribers:
        :return:
        """

        # Validate all subscribers received expected amount of messages
        expected_count = self.MESSAGES * len(routers)
        receiver_results = [(s.container_id,
                             s.received,
                             s.received == expected_count) for s in subscribers]
        assert all([res[2] for res in receiver_results]), \
            "Unable to receive %d messages through receivers: %s" % \
            (expected_count, ["%s=%d" % (res[0], res[1]) for res in receiver_results if not res[2]])

        # Validating received message contents (integrity)
        sha1_sum = hashlib.sha1(sent_body.encode('utf-8')).hexdigest()

        # Checking integrity on all received messages across all routers
        # Ensure there are subscribers
        assert subscribers
        for s in subscribers:
            # Ensure there are messages to be validated
            assert s.messages
            for m in s.messages:
                res_sha1_sum = hashlib.sha1(m.encode('utf-8')).hexdigest()
                assert res_sha1_sum == sha1_sum, 'Received message content is not expected on %s' % s.container_id

    def validate_all_messages_sent(self, publishers):
        """
        Validates the results for the provided list of publishers. The following
        validation(s) is(are) performed:
        - Assert that each sender was able to deliver the pre-defined amount of messages (self.MESSAGES)
        :param publishers:
        :return:
        """
        sender_results = [(p.sender_id, p.sent == self.MESSAGES) for p in publishers]
        assert all([res[1] for res in sender_results]), \
            "Unable to send %d messages through senders: %s" % \
            (self.MESSAGES, [res[0] for res in sender_results if not res[1]])

    def test_synchronous_durable_subscription(self, topic_durable, broker, iqa: Instance):
        """
        Connects one Durable Subscriber to the "topic_durable" address across all routers.
        Once all subscribers are connected, it starts one Publisher against each router
        in the topology.
        Next the test waits till all senders are done and till all receivers are done receiving (or timed-out).
        Then it validates:
        - Number of messages sent
        - Number of messages received by each receiver (expecting self.MESSAGES * len(routers))
        - Integrity of received messages by comparing received body SHA1 with unique SHA1 sum from sent body.
        :param topic_durable: Fixture that provides the topic to send/receive from
        :param broker: A Broker component instance (not being used yet, but illustrates which broker is being used)
        :param iqa: IQAInstance fixture that provides a list with all routers that will be used
        :return:
        """

        # Broker instance
        broker_instance = iqa.get_brokers(broker)[0]
        assert broker_instance

        # List of routers to use
        routers = iqa.get_routers()

        # Create subscriber list
        subscribers = self.create_subscribers(routers, topic_durable, durable=True)

        # Wait till all receivers have been created
        while not all(s.receiver for s in subscribers):
            time.sleep(TestDurableNonDurableSubscription.DELAY)

        # Create publisher list
        publishers = self.create_publishers(routers, topic_durable)

        # Wait till all publishers and subscribers done
        # the stopped flag will turn into true if any of them times out
        [p.join() for p in publishers]
        [s.join() for s in subscribers]

        # Assert all senders sent correct amount of messages
        self.validate_all_messages_sent(publishers)

        # Assert that all receivers received expected amount of messages
        self.validate_all_messages_received(publishers[0].message_body, routers, subscribers)

    def test_asynchronous_durable_subscription(self, topic_durable, broker, iqa: Instance):
        """
        This test must be defined as the second one (as tests defined in classes run sequentially in py.test).
        With that said, the previous test left the durable subscriptions available in the related Broker instance.
        So when this test runs, the Publishers will run first and will publish a pre-defined (self.MESSAGES) number
        of messages into the related multicast address (topic_durable).
        It waits till all publishers are done sending (or timed-out).
        Next it will connect one Durable Subscriber instance with the "topic_durable" address across all routers
        in the topology. Then it waits till all receivers are done receiving (or timed-out).
        Then it validates:
        - Number of messages sent
        - Number of messages received by each receiver (expecting self.MESSAGES * len(routers))
        - Integrity of received messages by comparing received body SHA1 with unique SHA1 sum from sent body.
        :param topic_durable: Fixture that provides the topic to send/receive from
        :param broker: A Broker component instance (not being used yet, but illustrates which broker is being used)
        :param iqa: IQAInstance fixture that provides a list with all routers that will be used
        :return:
        """

        # Broker instance
        broker_instance = iqa.get_brokers(broker)[0]
        assert broker_instance

        # List of routers to use
        routers = iqa.get_routers()

        # Create publisher list
        publishers = self.create_publishers(routers, topic_durable)

        # Wait till all senders have delivered their messages
        [p.join() for p in publishers]

        # Assert all senders sent correct amount of messages
        self.validate_all_messages_sent(publishers)

        # Create subscriber list
        # At this point, as previous test (synchronous) completed, a durable subscription already
        # exists, so subscribers should be able to retrieve their messages properly now
        subscribers = self.create_subscribers(routers, topic_durable, durable=True)

        # Wait till all subscribers are done
        # the stopped flag will turn into true if any of them times out
        [s.join() for s in subscribers]

        # Assert that all receivers received expected amount of messages
        self.validate_all_messages_received(publishers[0].message_body, routers, subscribers)

    def test_synchronous_nondurable_subscription(self, topic_nondurable, broker, iqa: Instance):
        """
        Connects one Non-Durable Subscriber instance to the "topic_durable" address across all routers.
        Once all subscribers are connected, it starts one Publisher against each router
        in the topology.
        Next the test waits till all senders are done and till all receivers are done receiving (or timed-out).
        Then it validates:
        - Number of messages sent
        - Number of messages received by each receiver (expecting self.MESSAGES * len(routers))
        - Integrity of received messages by comparing received body SHA1 with unique SHA1 sum from sent body.
        :param topic_nondurable: Fixture that provides the topic to send/receive from
        :param broker: A Broker component instance (not being used yet, but illustrates which broker is being used)
        :param iqa: IQAInstance fixture that provides a list with all routers that will be used
        :return:
        """

        # Broker instance
        broker_instance = iqa.get_brokers(broker)[0]
        assert broker_instance

        # List of routers to use
        routers = iqa.get_routers()

        # Create subscriber list
        subscribers = self.create_subscribers(routers, topic_nondurable, durable=False)

        # Wait till all receivers have been created
        while not all(s.receiver for s in subscribers):
            time.sleep(TestDurableNonDurableSubscription.DELAY)

        # Create publisher list
        publishers = self.create_publishers(routers, topic_nondurable)

        # Wait till all publishers and subscribers done
        # the stopped flag will turn into true if any of them times out
        [p.join() for p in publishers]
        [s.join() for s in subscribers]

        # Assert all senders sent correct amount of messages
        self.validate_all_messages_sent(publishers)

        # Assert that all receivers received expected amount of messages
        self.validate_all_messages_received(publishers[0].message_body, routers, subscribers)

    def test_asynchronous_nondurable_subscription(self, topic_nondurable, broker, iqa: Instance):
        """
        Publishers run first and will publish a pre-defined (self.MESSAGES) number of messages into the related
        multi-cast address (topic_nondurable).
        It waits till all publishers are done sending (or timed-out).
        Next it will connect one Non-Durable Subscriber instance with the "topic_nondurable" address across all routers
        in the topology. Then it waits till all receivers time-out.
        Then it validates:
        - Number of messages sent
        - Expect all receivers to time-out
        - Number of messages received by each receiver (expecting 0)
        :param topic_nondurable: Fixture that provides the topic to send/receive from
        :param broker: A Broker component instance (not being used yet, but illustrates which broker is being used)
        :param iqa: IQAInstance fixture that provides a list with all routers that will be used
        :return:
        """

        async_timeout = 30

        broker_instance = iqa.get_brokers(broker)[0]
        assert broker_instance

        # List of routers to use
        routers = iqa.get_routers()

        # Create subscriber list
        subscribers = self.create_subscribers(routers, topic_nondurable, durable=False, timeout=async_timeout)

        # Wait till all receivers have been created
        while not all(s.receiver for s in subscribers):
            time.sleep(TestDurableNonDurableSubscription.DELAY)

        # Now stop all receivers to ensure non-durable subscription was discarded
        [s.stop_receiver() for s in subscribers]

        # Create publisher list
        publishers = self.create_publishers(routers, topic_nondurable)

        # Wait till all publishers are done sending
        [p.join() for p in publishers]

        # Create subscribers now with a small timeout and expect nothing to be received
        subscribers = self.create_subscribers(routers, topic_nondurable, durable=False, timeout=async_timeout)

        # Wait till all subscribers timeout
        [s.join() for s in subscribers]

        # Assert all senders sent correct amount of messages
        self.validate_all_messages_sent(publishers)

        # Assert that all receivers did not receive any message and that all of them timed out
        assert all([s.received == 0 for s in subscribers]), "Expecting no message received"
        assert all([s.timeout_handler.timed_out() for s in subscribers]), "Expecting all receivers to timeout"
