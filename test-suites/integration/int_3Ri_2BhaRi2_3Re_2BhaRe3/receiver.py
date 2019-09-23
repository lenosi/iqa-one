"""
A custom receiver implementation that can be used, as an alternative,
for testing Edge Router topology.
"""
import threading
import logging

from proton.handlers import MessagingHandler
from proton.reactor import Container, DurableSubscription

from iqa.utils.timeout import TimeoutCallback


class Receiver(MessagingHandler, threading.Thread):
    """
    Receiver implementation of a Proton client that run as a thread.
    """
    def __init__(self, url, message_count, timeout=0, container_id=None, durable=False, save_messages=False,
                 ignore_dups=False):
        super(Receiver, self).__init__()
        threading.Thread.__init__(self)
        self.url = url
        self.receiver = None
        self.connection = None
        self.received = 0
        self.total = message_count
        self.timeout_secs = timeout
        self.timeout_handler = None
        self.container_id = container_id
        self.container = None
        self.durable = durable
        self.last_received_id = {}
        self.messages = []
        self.save_messages = save_messages
        self.ignore_dups = ignore_dups
        self._stopped = False

    def run(self):
        """
        Starts the thread and the Proton container
        :return:
        """
        # If a timeout has been given, use it
        if self.timeout_secs > 0:
            self.timeout_handler = TimeoutCallback(self.timeout_secs, self.stop_receiver)

        self.container = Container(self)
        self.container.container_id = self.container_id
        self.container.run()

        # If receiver gets disconnected from remote peer, stop receiver
        self.stop_receiver()

    def on_start(self, event):
        """
        Creates the receiver
        :param event:
        :return:
        """
        subs_opts = None
        if self.durable:
            subs_opts = DurableSubscription()
        self.receiver = event.container.create_receiver(self.url, name=self.container_id, options=subs_opts)
        self.connection = self.receiver.connection

    def on_message(self, event):
        """
        Processes an incoming message
        :param event:
        :return:
        """

        # Ignore received message from user id
        if self.ignore_dups and event.message.user_id and event.message.id and \
                event.message.user_id in self.last_received_id and \
                self.last_received_id[event.message.user_id] == event.message.id:
            logging.warning('Ignoring duplicated message [id: %s]' % event.message.id)
            return

        logging.debug("%s - received message" % self.container_id)
        self.last_received_id[event.message.user_id] = event.message.id
        self.received += 1

        # Saving received message for further validation
        if self.save_messages:
            self.messages.append(event.message.body)

        # Validate if receiver is done receiving
        if self.is_done_receiving():
            self.stop_receiver(event.receiver, event.connection)

    def stop_receiver(self, receiver=None, connection=None):
        """
        Stops the receiver. If durable flag is set, then it simply detaches in
        order to preserve the subscription.
        :param receiver:
        :param connection:
        :return:
        """
        if self._stopped:
            return

        if self.timeout_handler:
            self.timeout_handler.interrupt()

        self._stopped = True
        rec = receiver or self.receiver
        con = connection or self.connection

        # When using durable subscription, detach first (or subscription will be removed)
        if self.durable:
            rec.detach()

        if rec:
            rec.close()
        if con:
            con.close()

    def is_done_receiving(self):
        """
        Validates if all messages have been received (when expecting a
        positive amount of messages)
        :return:
        """
        return self.stopped or (self.total > 0 and (self.received == self.total))

    @property
    def stopped(self):
        """
        Returns a bool. True if receiver has stopped (completed or timed out)
        :return:
        """
        return self._stopped
