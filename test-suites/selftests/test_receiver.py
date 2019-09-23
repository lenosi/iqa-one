from iqa.messaging_abstract.client import Receiver


def test_isinstance(receiver: Receiver):
    """
    Check if created receiver is instance of Receiver class.
    :param receiver:
    """
    assert isinstance(receiver, Receiver)


def test_name(receiver: Receiver):
    """
    Check if created receiver is available in the test-suite.
    :param receiver:
    """
    clients = ['Internal core client', 'NodeJS RHEA client', 'Python Proton client']
    assert (receiver.name in clients) is True


def test_execute(receiver: Receiver):
    """
    Check remote command exec.
    :param receiver:
    """
    pass
