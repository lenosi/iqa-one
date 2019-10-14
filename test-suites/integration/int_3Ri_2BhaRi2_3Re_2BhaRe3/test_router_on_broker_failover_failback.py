import time

from iqa.system.service.service import ServiceStatus
from iqa.components.routers import Dispatch
from iqa.components.brokers import Artemis
from iqa.components.routers.dispatch.management import RouterQuery

from .receiver import Receiver
from .sender import Sender


class TestRouterOnBrokerFailOverFailBack(object):
    """
    Validates that all routers that have a connection to a Broker pair (HA), in Edge Router
    topology, received the correct failoverUrls list from Broker, have active autolinks and
    are able to exchange messages through linkRoutes and autoLinks using all pre-defined
    broker queues across all routers in the topology (edge and interior).
    The test is performed in three phases:
    - Initial (after deployment)
    - After Fail-over (Master broker stopped)
    - After Fail-back (Master broker restarted)
    """

    # Static parameters
    MESSAGE_COUNT = 10
    MESSAGE_SIZE = 1024
    TIMEOUT = 30

    @staticmethod
    def _get_router_query(router: Dispatch) -> RouterQuery:
        """
        Creates a RouterQuery based on provided Router instance
        :param router:
        :return:
        """
        query = RouterQuery(host=router.node.get_ip(),
                            port=router.port,
                            router=router)
        return query

    @staticmethod
    def validate_broker_connector_has_failoverurls(router):
        """
        Validate provided router instance has at least one route-container connector,
        and that the connector has the "failoverUrls" property set and it defines at least two urls.
        :param router:
        :return:
        """
        # Ensure that a router instance has been provided
        assert isinstance(router, Dispatch)

        # Wait for 30 seconds to router recovered from failover/failback
        time.sleep(30)

        # Creates an instance of the RouterQuery class and retrieve autolinks and connectors
        query = TestRouterOnBrokerFailOverFailBack._get_router_query(router)

        # Changed to true if at least one connector has been found
        connector_found = False

        # Retrieving all connectors
        for connector in query.connector():
            # ignore connectors to other routers
            if connector.role != 'route-container':
                continue

            # One route-container connector found
            connector_found = True

            # Connector must have failOverUrls defined and it must have more than 1 url
            assert connector.failoverUrls
            assert ',' in connector.failoverUrls

        assert connector_found is True

    @staticmethod
    def validate_autolinks_active(router):
        """
        Validates that all autolinks are in active state for provided router instance.
        :param router:
        :return:
        """
        # Ensure that a router instance has been provided
        assert isinstance(router, Dispatch)

        # Creates an instance of the RouterQuery class and retrieve autolinks and connectors
        query = TestRouterOnBrokerFailOverFailBack._get_router_query(router)

        # Ensure all autolinks are in "active" status
        max_attempts = 10
        attempt = 0
        all_autolinks_active = False

        while not all_autolinks_active and attempt < max_attempts:
            inactive = 0
            for autolink in query.config_autolink():
                if autolink.operStatus != 'active':
                    inactive += 1
            all_autolinks_active = inactive == 0
            attempt += 1
            time.sleep(10)

        assert all_autolinks_active

    def send_and_receive(self, queue, router):
        """
        Send and receive messages through the given router, using the
        provided queue as the address.

        Asserts that all messages are sent and received.
        :param queue:
        :param router:
        :return:
        """

        # URL to be used for sending/receiving (through broker queues)
        url = "amqp://%s:%s/%s" % (router.node.get_ip(), router.port, queue)
        # Creating a sender on the given address
        sender = Sender(url, self.MESSAGE_COUNT, sender_id=router.node.hostname,
                        message_size=self.MESSAGE_SIZE, timeout=self.TIMEOUT)
        sender.start()

        # Wait for sender to complete or timeout
        while not sender.stopped:
            pass

        # Validate all messages were sent
        assert sender.sent == self.MESSAGE_COUNT

        # Creating a receiver now
        receiver = Receiver(url=url, message_count=self.MESSAGE_COUNT, timeout=self.TIMEOUT)
        receiver.start()

        # Waiting till all messages received or timed out
        while not receiver.stopped:
            pass

        # Validate all messages have been received
        assert receiver.received == self.MESSAGE_COUNT

    def broker_has_queues(self, broker):
        """
        Assert that the provided broker instance has queues.
        It attempts to retrieve queues "max_attempts" times with a delay of 1 between attempts.
        :param broker:
        :return:
        """
        max_attempts = 10
        attempt = 0

        while not broker.queues() and attempt < max_attempts:
            time.sleep(10)
            attempt += 1

        assert len(broker.queues()) > 0

    def test_initial_state(self, broker_m_internal: Artemis, broker_s_internal: Artemis,
                           broker_m_edge: Artemis, broker_s_edge: Artemis, router_i2: Dispatch, router_e3: Dispatch):
        """
        Sanity check to ensure all elements needed for testing are present
        :param broker_m_internal:
        :param broker_s_internal:
        :param broker_m_edge:
        :param broker_s_edge:
        :param router_i2:
        :param router_e3:
        :return:
        """
        assert broker_m_internal is not None
        assert broker_s_internal is not None
        assert broker_m_edge is not None
        assert broker_s_edge is not None
        assert router_i2 is not None
        assert router_e3 is not None

        assert len(broker_m_internal.queues()) > 0
        assert len(broker_m_edge.queues()) > 0
        assert len(broker_s_internal.queues()) == 0
        assert len(broker_s_edge.queues()) == 0

    def test_validate_broker_connector_initial_state(self, router_with_broker):
        """
        Validate initial state of router connector to broker
        :param router_with_broker:
        :return:
        """
        self.validate_broker_connector_has_failoverurls(router_with_broker)

    def test_validate_autolinks_initial_state(self, router_with_broker):
        """
        Validate initial state of autolinks to broker
        :param router_with_broker:
        :return:
        """
        self.validate_autolinks_active(router_with_broker)

    def test_exchange_messages_initial_state(self, router, queue):
        """
        Exchange messages to ensure initial state is working fine
        :param router:
        :param queue:
        :return:
        """
        self.send_and_receive(queue, router)

    def test_broker_failover(self, broker_master: Artemis):
        """
        Stops the provided master broker instance and ensure it has been stopped.
        :param broker_master:
        :return:
        """
        broker_master.service.stop()
        assert broker_master.service.status() == ServiceStatus.STOPPED

    def test_broker_slave_active(self, broker_slave: Artemis):
        """
        Wait till slave broker shows queues replicated from master broker (active).
        :param broker_slave:
        :return:
        """
        self.broker_has_queues(broker_slave)

    def test_validate_broker_connector_after_failover(self, router_with_broker):
        """
        Validate state of router connector to broker after fail-over
        :param router_with_broker:
        :return:
        """
        self.validate_broker_connector_has_failoverurls(router_with_broker)

    def test_validate_autolinks_after_failover(self, router_with_broker):
        """
        Validate state of autolinks to broker after fail-over
        :param router_with_broker:
        :return:
        """
        self.validate_autolinks_active(router_with_broker)

    def test_exchange_messages_after_failover(self, router, queue):
        """
        Exchange messages to ensure router has recovered from broker fail-over.
        :param router:
        :param queue:
        :return:
        """
        self.send_and_receive(queue, router)

    def test_broker_failback(self, broker_master: Artemis):
        """
        Starts the provided master broker instance and ensure it has been started.
        :param broker_master:
        :return:
        """
        broker_master.service.start()
        assert broker_master.service.status() == ServiceStatus.RUNNING

    def test_broker_master_active(self, broker_master: Artemis):
        """
        Wait till master broker shows queues again (active).
        :param broker_master:
        :return:
        """
        self.broker_has_queues(broker_master)

    def test_validate_broker_connector_after_failback(self, router_with_broker):
        """
        Validate state of router connector to broker after fail-back
        :param router_with_broker:
        :return:
        """
        self.validate_broker_connector_has_failoverurls(router_with_broker)

    def test_validate_autolinks_after_failback(self, router_with_broker):
        """
        Validate state of autolinks to broker after fail-back
        :param router_with_broker:
        :return:
        """
        self.validate_autolinks_active(router_with_broker)

    def test_exchange_messages_after_failback(self, router, queue):
        """
        Exchange messages to ensure router has recovered from broker fail-back.
        :param router:
        :param queue:
        :return:
        """
        self.send_and_receive(queue, router)
