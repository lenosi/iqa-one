"""PyTest fixtures."""
from typing import Optional

import pytest

from iqa.components.clients.external.java.receiver import ReceiverJava
from iqa.components.clients.external.java.sender import SenderJava
from iqa.components.clients.external.python.receiver import ReceiverPython
from iqa.components.clients.external.python.sender import SenderPython
from iqa.components.clients.external.nodejs.receiver import ReceiverNodeJS
from iqa.components.clients.external.nodejs.sender import SenderNodeJS
from iqa.instance.instance import Instance
from iqa.utils.types import ComponentType, ReceiverType, SenderType, RouterType, ReceiverSubtype


@pytest.fixture()
def iqa(request) -> Instance:
    return request.config.iqa


def first_or_none(components: list) -> Optional[ComponentType]:
    """
    Returns first component provided or None
    :param components:
    :return:
    """
    if components:
        return components[0]
    return None


@pytest.fixture()
def router(iqa: Instance) -> Optional[RouterType]:
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
    return first_or_none(iqa.get_clients(ReceiverSubtype, 'java'))


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
