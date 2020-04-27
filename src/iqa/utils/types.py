from typing import TypeVar, Union

from iqa.abstract.client.client import Client
from iqa.abstract.client.receiver import Receiver
from iqa.abstract.client.sender import Sender
from iqa.abstract.server.broker import Broker
from iqa.abstract.server.router import Router
from iqa.components.abstract.component import Component
from iqa.components.abstract.management.client import ManagementClient
from iqa.system.executor import Executor
from iqa.system.node.node import Node

BrokerSubtype = TypeVar('BrokerSubtype', bound=Broker)
BrokerType = Union[BrokerSubtype, Broker]

ClientSubtype = TypeVar('ClientSubtype', bound=Client)
ClientType = Union[ClientSubtype, Client]

ComponentSubtype = TypeVar('ComponentSubtype', bound=Component)
ComponentType = Union[ComponentSubtype, Component]

ExecutorSubtype = TypeVar('ExecutorSubtype', bound=Executor)
ExecutorType = Union[ExecutorSubtype, Executor]

ManagementClientSubtype = TypeVar('ManagementClientSubtype', bound=ManagementClient)
ManagementClientType = Union[ManagementClientSubtype, ManagementClient]

NodeSubtype = TypeVar('NodeSubtype', bound=Node)
NodeType = Union[NodeSubtype, Node]

RouterSubtype = TypeVar('RouterSubtype', bound=Router)
RouterType = Union[RouterSubtype, Router]

ReceiverSubtype = TypeVar('ReceiverSubtype', bound=Receiver)
ReceiverType = Union[ReceiverSubtype, Receiver]

SenderSubtype = TypeVar('SenderSubtype', bound=Sender)
SenderType = Union[SenderSubtype, Sender]
