from iqa.abstract.client import Sender
from odict import odict


def test_isinstance(sender: Sender):
    """
    Check if created sender is instance of Sender class.
    :param sender:
    """
    assert isinstance(sender, Sender)


def test_name(sender: Sender):
    """
    Check if created sender is available in the test-suite.
    :param sender:
    """
    clients = ['Internal core client', 'NodeJS RHEA client', 'Python Proton client']
    assert (sender.name in clients) is True


def test_execute(sender: Sender):
    """
    Check remote command exec.
    :param sender:
    """
    pass
