import abc
import logging
from typing import List

from iqa.messaging.abstract.destination.address import Address
from iqa.messaging.abstract.destination.queue import Queue
from iqa.messaging.abstract.server.messaging_server import MessagingServer


class Broker(MessagingServer):
    """
    Abstract broker class
    """
    supported_protocols = []

    def __init__(self, name: str, **kwargs):
        super(Broker, self).__init__()

        # Log missing arguments
        required_fields = ['broker_name', 'broker_path']
        for field in required_fields:
            if field not in kwargs:
                logging.error("Missing requirement broker parameter: %s" % field)

        self.broker_name = kwargs.get('broker_name')
        self.broker_path = kwargs.get('broker_path')
        self.web_port = kwargs.get('broker_web_port', 8161)
        self.user = kwargs.get('broker_user', 'admin')
        self.password = kwargs.get('broker_password', 'admin')
        self.cluster_member = None
        self.ha_member = None

    def set_cluster_member(self, cluster_component):
        self.cluster_member = cluster_component

    def set_ha_member(self, ha_component):
        self.ha_member = ha_component

    @abc.abstractmethod
    def queues(self, refresh: bool = True) -> List[Queue]:
        """
        Must return existing queues
        :return:
        """
        pass

    @abc.abstractmethod
    def addresses(self, refresh: bool = True) -> List[Address]:
        """
        Must return existing addresses
        :return:
        """
        pass
