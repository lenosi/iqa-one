"""
A custom receiver implementation that can be used, as an alternative,
for testing Edge Router topology.
"""
import threading
import logging
from typing import Optional

from proton import Connection, Event, Receiver as ProtonReceiver
from proton.handlers import MessagingHandler
from proton.reactor import Container, DurableSubscription

from iqa.utils.timeout import TimeoutCallback


class Receiver(MessagingHandler, threading.Thread):
    """
    Receiver implementation of a Proton client that run as a thread.
    """
    def __init__(self, url: str, message_count: int, timeout: int = 0, container_id: str = None, durable: bool = False,
                 save_messages: bool = False, ignore_dups: bool = False) -> None:
        super(Receiver, self).__init__()
        threading.Thread.__init__(self)
        self.url: str = url
        self.receiver: Optional[ProtonReceiver] = None
        self.connection: Optional[Connection] = None
        self.received: int = 0
        self.total: int = message_count
        self.timeout_secs: int = timeout
        self.timeout_handler: Optional[TimeoutCallback] = None
        self.container_id: str = container_id
        self.container: Optional[Container] = None
        self.durable: bool = durable
        self.last_received_id: dict = {}
        self.messages: list = []
        self.save_messages: bool = save_messages
        self.ignore_dups: bool = ignore_dups
        self._stopped: bool = False

    def run(self) -> None:
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

    def on_start(self, event: Event) -> None:
        """
        Creates the receiver
        :param event:
        :return:
        """
        subs_opts: Optional[DurableSubscription] = None
        if self.durable:
            subs_opts = DurableSubscription()
        self.receiver = event.container.create_receiver(self.url, name=self.container_id, options=subs_opts)
        self.connection = self.receiver.connection

    def on_message(self, event: Event) -> None:
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

    def stop_receiver(self, receiver: ProtonReceiver = None, connection: Connection = None):
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
        rec: ProtonReceiver = receiver or self.receiver
        con: Connection = connection or self.connection

        # When using durable subscription, detach first (or subscription will be removed)
        if self.durable:
            rec.detach()

        if rec:
            rec.close()
        if con:
            con.close()

    def is_done_receiving(self) -> bool:
        """
        Validates if all messages have been received (when expecting a
        positive amount of messages)
        :return:
        """
        return self.stopped or (self.total > 0 and (self.received == self.total))

    @property
    def stopped(self) -> bool:
        """
        Returns a bool. True if receiver has stopped (completed or timed out)
        :return:
        """
        return self._stopped
