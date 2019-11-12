"""PyTest fixtures."""
from typing import Optional, TypeVar

import pytest

from iqa.abstract import Receiver, Router, Sender
from iqa.components.abstract.component import Component
from iqa.components.clients.external.java import ReceiverJava, SenderJava
from iqa.components.clients.external.python import ReceiverPython, SenderPython
from iqa.components.clients.external.nodejs import ReceiverNodeJS, SenderNodeJS
from iqa.instance.instance import Instance

CmpType = TypeVar('CmpType', bound=Component)
ReceiverType = TypeVar('ReceiverType', bound=Receiver)
SenderType = TypeVar('SenderType', bound=Sender)


@pytest.fixture()
def iqa(request) -> Instance:
    return request.config.iqa


def first_or_none(components: list) -> Optional[CmpType]:
    """
    Returns first component provided or None
    :param components:
    :return:
    """
    if components:
        return components[0]
    return None


@pytest.fixture()
def router(iqa: Instance) -> Optional[Router]:
    """
    Returns the first Router instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_routers())


@pytest.fixture()
def java_receiver(iqa: Instance) -> Optional[ReceiverJava]:
    """
    Returns the first Java Receiver instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(ReceiverType, 'java'))


@pytest.fixture()
def java_sender(iqa: Instance) -> Optional[SenderJava]:
    """
    Returns the first Java Sender instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(SenderType, 'java'))


@pytest.fixture()
def python_receiver(iqa: Instance) -> Optional[ReceiverPython]:
    """
    Returns the first Python Receiver instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(ReceiverType, 'python'))


@pytest.fixture()
def python_sender(iqa: Instance) -> Optional[SenderPython]:
    """
    Returns the first Python Sender instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(SenderType, 'python'))


@pytest.fixture()
def nodejs_receiver(iqa: Instance) -> Optional[ReceiverNodeJS]:
    """
    Returns the first NodeJS Receiver instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(ReceiverType, 'nodejs'))


@pytest.fixture()
def nodejs_sender(iqa: Instance) -> Optional[SenderNodeJS]:
    """
    Returns the first NodeJS Sender instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(SenderType, 'nodejs'))
