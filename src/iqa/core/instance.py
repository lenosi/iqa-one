"""
IQAInstance which is populated based on an ansible compatible inventory file.
"""
from typing import List

from autologging import logged, traced

from iqa.messaging.abstract.client import Client
from iqa.messaging.abstract.client.receiver import Receiver
from iqa.messaging.abstract.client.sender import Sender
from iqa.messaging.abstract.server.broker import Broker
from iqa.messaging.abstract.server.router import Router
from iqa.system.ansible.ansible_inventory import AnsibleInventory
from iqa.system.executor import ExecutorFactory
from iqa.components.abstract.component import *
from iqa.components.brokers import BrokerFactory
from iqa.components.clients import ClientFactory
from iqa.components.routers import RouterFactory
from iqa.system.node import NodeFactory
from iqa.system.service import *


# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
@logged
@traced
class IQAInstance:
    """IQA helper class

    Store variables, node and related things
    """
    def __init__(self, inventory='', cli_args: dict=None):
        self.inventory = inventory
        self._inv_mgr = AnsibleInventory(inventory=self.inventory, extra_vars=cli_args)
        self.nodes = []
        self.components = []
        self._load_components()

    def _load_components(self):
        """
        Parses the mandatory ansible inventory file and load all defined
        messaging components.
        :return:
        """

        def get_and_remove_key(vars_dict: dict, key: str, default: str=None):
            val = vars_dict.get(key, default)
            if key in vars_dict:
                del vars_dict[key]
            return val

        # Loading all hosts that provide the component variable
        inventory_hosts = self._inv_mgr.get_hosts_containing(var='component')
        components = []
        nodes = []

        for cmp in inventory_hosts:
            # Make a shallow copy (important as retrieved keys are deleted)
            # print('ansible host = %s' % cmp)
            cmp_vars = dict(self._inv_mgr.get_host_vars(host=cmp))

            # Common variables across all component types
            cmp_type = get_and_remove_key(cmp_vars, 'component')
            cmp_impl = get_and_remove_key(cmp_vars, 'implementation')
            cmp_exec = get_and_remove_key(cmp_vars, 'executor', 'ansible')
            cmp_ip = cmp_vars.get('ansible_host', None)

            # Getting the executor instance
            executor = ExecutorFactory.create_executor(exec_impl=cmp_exec, **cmp_vars)

            # Create the Node for current client
            node = NodeFactory.create_node(hostname=cmp.name, executor=executor, ip=cmp_ip)
            nodes.append(node)

            # Now loading variables that are specific to each component
            if cmp_type == 'client':
                # Add list of clients into component list
                components += ClientFactory.create_clients(implementation=cmp_impl, node=node, executor=executor,
                                                           **cmp_vars)
            elif cmp_type in ['router', 'broker']:
                # A service name is expected
                cmp_svc = get_and_remove_key(cmp_vars, 'service')
                svc = ServiceFactory.create_service(executor=executor, service_name=cmp_svc, **cmp_vars)

                if cmp_type == 'router':
                    components.append(RouterFactory.create_router(implementation=cmp_impl, node=node, executor=executor,
                                                                  service_impl=svc, **cmp_vars))
                elif cmp_type == 'broker':
                    components.append(BrokerFactory.create_broker(implementation=cmp_impl, node=node, executor=executor,
                                                                  service_impl=svc, **cmp_vars))

        self.nodes = nodes
        self.components = components

    def new_node(self, hostname, ip=None):
        """Create new node under iQA instance

        @TODO dlenoch Pass inventory by true way for Ansible
        # TODO jstejska: Description

        :param hostname:
        :type hostname:
        :param ip:
        :type ip:

        :return:
        :rtype:
        """
        node = Node(hostname=hostname, ip=ip, ansible=self.ansible)
        self.nodes.append(node)
        return node

    def new_component(self, node: Node, component):
        """Create new node under iQA instance

        @TODO Pass inventory by true way for Ansible

        :param node:
        :type node:
        :param component:
        :type component:

        :return:
        :rtype:
        """
        self.components.append(component)
        return component

    @property
    def brokers(self):
        """
        Get all broker instances on this node
        :return:
        """
        return [component for component in self.components
                if isinstance(component, Broker)]

    @property
    def clients(self):
        """
        Get all client instances on this node
        @TODO
        :return:
        """
        return [component for component in self.components
                if isinstance(component, Client)]

    def get_clients(self, client_type: type, implementation: str=None):
        """
        Get all client instances on this node
        @TODO
        :return:
        """
        return [component for component in self.clients
                if isinstance(component, client_type) and
                (implementation is None or
                component.implementation == implementation.lower())]

    def get_receiver(self, hostname: str):
        """
        Return a single receiver running on provided hostname.
        :param hostname:
        :return: the receiver implementation running on given host
                 or None otherwise.
        """
        for receiver in self.get_clients(client_type=Receiver):
            if receiver.node.hostname == hostname:
                return receiver
        return None

    def get_sender(self, hostname: str):
        """
        Return a single sender running on provided hostname.
        :param hostname:
        :return: the sender implementation running on given host
                 or None otherwise.
        """
        for sender in self.get_clients(client_type=Sender):
            if sender.node.hostname == hostname:
                return sender
        return None

    @property
    def routers(self):
        """
        Get all router instances on this node
        :return:
        """
        return [component for component in self.components
                if isinstance(component, Router)]

    def get_routers(self, hostname: str = None) -> List[Router]:
        """
        Get all router instances on this node
        :type hostname: optional hostname
        :return:
        """
        return [component for component in self.routers
                if not hostname or component.node.hostname == hostname]

    def get_brokers(self, hostname: str = None) -> List[Broker]:
        """
        Get all broker instances on this node
        :type hostname: optional hostname
        :return:
        """
        return [component for component in self.brokers
                if not hostname or component.node.hostname == hostname]
